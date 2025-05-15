from typing_extensions import Annotated
import os, ast, subprocess, shutil, tempfile, re
from collections import Counter

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.summary = {'classes': [], 'functions': []}
        self.current_calls = []

    def visit_ClassDef(self, node):
        class_info = {
            'name': node.name,
            'line': node.lineno,
            'methods': []
        }
        self.summary['classes'].append(class_info)
        self.stack.append(('class', class_info))
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node):
        full_name = []
        for item in self.stack:
            if item[0] in ['class', 'function']:
                full_name.append(item[1]['name'])
        full_name.append(node.name)
        full_name = '.'.join(full_name)

        args = self.get_arguments(node.args)

        function_info = {
            'name': full_name,
            'line': node.lineno,
            'args': args,
            'calls': []
        }

        in_class = any(item[0] == 'class' for item in self.stack)
        if in_class:
            for item in reversed(self.stack):
                if item[0] == 'class':
                    item[1]['methods'].append(function_info)
                    break
        else:
            self.summary['functions'].append(function_info)

        self.stack.append(('function', function_info))
        self.current_calls = []
        self.generic_visit(node)
        function_info['calls'] = self.current_calls.copy()
        self.stack.pop()

    def visit_Call(self, node):
        call_name = self.get_call_name(node.func)
        if call_name:
            self.current_calls.append(call_name)
        self.generic_visit(node)

    def get_call_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.get_call_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self.get_call_name(node.func)
        else:
            return None

    def get_arguments(self, args_node):
        args = []
        if hasattr(args_node, 'posonlyargs'):
            args.extend([arg.arg for arg in args_node.posonlyargs])
        args.extend([arg.arg for arg in args_node.args])
        if args_node.vararg:
            args.append(f"*{args_node.vararg.arg}")
        args.extend([arg.arg for arg in args_node.kwonlyargs])
        if args_node.kwarg:
            args.append(f"**{args_node.kwarg.arg}")
        return args

def search_root(
        root_folder: Annotated[str, ..., "Root folder path to search"],
        search_name: Annotated[str, ..., "Name to match"]
        ) -> str:
    """
    Search for files, folders in a root folder that have similar name.

    Args:
        root_folder: Root folder path.
        search_name: Name of files, folders to match

    Returns:
        A list of file, folder paths that match the given pattern.
    """
    matched_folders = []
    matched_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_folder):
        matched_folders.extend(os.path.join(dirpath, d) for d in dirnames if search_name in d)
        matched_files.extend(os.path.join(dirpath, f) for f in filenames if search_name in f)
    
    all_matches = matched_folders + matched_files
    
    # Count occurrences
    counter = Counter(all_matches)
    top_matches = counter.most_common(10)
    
    # Format output
    result = ''
    if len(top_matches) == 0:
        return f'{root_folder} does not contain any files, folder with name similar to "{search_name}"'
    elif len(top_matches) > 10:
        result = "\nTop 10 Matching Folders and Files:\n"
    for i, (path, count) in enumerate(top_matches, start=1):
        result += f"{i}. {path} (Occurrences: {count})\n"
    
    return result.strip()

def search_content(
    root: Annotated[str, ..., "Root folder path or file path to search within"],
    query: Annotated[str, ..., "Text string to search for within file contents"]
) -> str:
    """
    Search for a specific text string within all files under a root folder or a single file.

    Args:
        root: Root folder path or file path.
        query: Text string to search for within the file contents.

    Returns:
        A formatted string summarizing the search results, showing files and lines containing the query, or any errors encountered.
    """
    results = {}
    errors = []

    def search_in_file(file_path: str):
        """Helper function to search for query inside a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            matches = [i + 1 for i, line in enumerate(lines) if query in line]
            if matches:
                results[file_path] = matches
        except Exception as file_error:
            errors.append(f"Error reading file {file_path}: {file_error}")

    try:
        if os.path.isfile(root):  # If root is a file, search only in that file
            search_in_file(root)
        elif os.path.isdir(root):  # If root is a directory, search in all files within it
            for dirpath, _, filenames in os.walk(root):
                for filename in filenames:
                    if len(results) >= 10:
                        break  # Stop searching after finding 10 files
                    search_in_file(os.path.join(dirpath, filename))
        else:
            return f"Error: '{root}' is neither a valid file nor a folder."

    except Exception as e:
        return f"Error during content search: {e}"

    # Format output
    if not results and not errors:
        return "No matches found."

    result_str = "Search Results:\n" + "\n".join(
        f"{file_path}: Line(s) {', '.join(map(str, lines[:10]))}" + ('...' if len(lines) > 10 else '')
        for file_path, lines in results.items()
    )

    if len(results) == 10:
        result_str += "\n\nShowing top 10 files containing the query."

    if errors:
        result_str += "\n\nErrors Encountered:\n" + "\n".join(errors)

    return result_str.strip()

def edit_file(
    location: Annotated[str, "File path to edit"],
    line_number: Annotated[int, "Line number to modify (1-based)"],
    existing: Annotated[str, "Expected content starts from the specified line"],
    replacement: Annotated[str, "Replacement text to replace the existing content"]
) -> str:
    """
    Modify a file by replacing a block of existing content with replacement content, starting at a specified line. Ensures the existing content matches before applying the replacement and provides surrounding context.

    Args:  
        location: Path to the file to be modified, supporting formats like txt, py, csv, etc.  
        line_number: The 1-based starting line number where the old content is expected.  
        existing: The block of text to be replaced, which must start at the specified line and can span multiple lines.  
        replacement: The new content to replace the old block. Can span multiple lines.

    Returns:  
        A formatted message indicating success or failure, along with a preview of the surrounding lines. On success, displays the edited section. On failure, explains the issue with context.

    Note: `edit_file` REQUIRES PROPER INDENTATION. If you would like to replace the line '        print(x)', you must fully write that out, with all those spaces before the code!
    """

    try:
        line_number = int(line_number)
        # Check if file exists
        if not os.path.exists(location):
            return f"Error: File '{location}' does not exist."
        
        # Read file content
        with open(location, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        
        total_lines = len(lines)
        # Validate line number
        if line_number < 1 or line_number > total_lines:
            # Generate context for line number error
            context_start = max(0, line_number - 3)  # Show 3 lines before and after
            context_start = max(0, context_start -1)  # Convert to 0-based
            context_end = min(total_lines, line_number + 2)
            context = []
            for i in range(context_start, context_end):
                line_num = i + 1
                context.append(f"{line_num:4}    {lines[i]}")
            context_str = "\n".join(context)
            return (f"Error: Line number {line_number} is out of valid range (1-{total_lines}).\n"
                    f"Context around the specified line number:\n{context_str}")
        
        line_index = line_number - 1
        num_line_of_old_content = len(existing.split('\n'))
        original_line = '\n'.join(lines[line_index:line_index+num_line_of_old_content])
        
        # Check if the line starts with old_content
        if not original_line.startswith(existing):
            # Generate context for content mismatch error
            context_start = max(0, line_index - 2)
            context_end = min(len(lines), line_index + 3)
            context = []
            for i in range(context_start, num_line_of_old_content + line_number - 1):
                current_line_num = i + 1
                line = lines[i]
                if (num_line_of_old_content + line_number) > current_line_num >= line_number:
                    context.append(f"{current_line_num:4} >>|{line}")
                else:
                    context.append(f"{current_line_num:4}   |{line}")
            for i, text in zip(range(line_number - 1, num_line_of_old_content + line_number - 1), existing.split('\n')):
                current_line_num = i + 1
                context.append(f"{current_line_num:4} * |{text}")
            context_str = "\n".join(context)
            return (f"Error: Line {line_number} does not start with the expected content.\n"
                    f"Context around line {line_number} (>> original lines, * your wrong expected lines). "
                    f"Please ensure that your `existing` matches with `>>` lines:\n{context_str}")
        
        # Replace the line(s) with new_content
        new_lines = replacement.split('\n')
        # Update the lines list
        lines = lines[:line_index] + new_lines + lines[line_index + num_line_of_old_content:]
        
        # Write the modified content back to the file
        with open(location, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        # Generate success context
        modified_start = line_index
        modified_end = line_index + len(new_lines)
        context_start = max(0, modified_start - 2)
        context_end = min(len(lines), modified_end + 3)
        
        context = []
        for i in range(context_start, context_end):
            line_num = i + 1
            line = lines[i]
            if modified_start <= i < modified_end:
                context.append(f"{line_num:4} +-|{line}")
            else:
                context.append(f"{line_num:4}   |{line}")
        context_str = "\n".join(context)
        
        pylint_notification = ''
        if location.endswith('.py'):
            pylint_notification = "Pylint message for the file's content:\n" + check_pylint_errors(location)

        return (f"Successfully edited '{location}'\n"
                f"Replaced line {line_number} with new content.\n"
                f"Content after editing (lines {context_start + 1}-{context_end}):\n"
                f"{context_str}"
                f"{pylint_notification}")
    
    except Exception as e:
        return f"Error editing file '{location}': {str(e)}"
    
def view_file(
    location: Annotated[str, ..., "File path whose content is to be displayed"],
    start_line: Annotated[int, ..., "Line number to start displaying the content of the file, starts from 1"]
) -> str:
    """
    Retrieve and return the content of the specified file from a given start line.

    Args:
        location: Path to a file to show the file's content
        start_line: Line number to start displaying the content of the file, starts from 1.

    Returns:
        A formatted string containing up to 40 lines from the file.
        If an error occurs (e.g., file not found, path is not correct to a file, invalid start line), an appropriate error message is returned.
    """
    try:
        limit = 40

        start_line = int(start_line)

        if not os.path.exists(location):
            return f"Error: The file '{location}' does not exist."

        if not os.path.isfile(location):
            if os.path.isdir(location):
                return f"Error: '{location}' is a directory, not a file. `view_file` cannot be used here. Use `list_dir` to view files and folders instead."
            return f"Error: '{location}' is not a path to a file."

        with open(location, 'r', encoding='utf-8') as f:
            contents = f.readlines()
        
        total_lines = len(contents)

        if start_line < 1 or start_line > total_lines:
            return f"Error: Start line {start_line} is out of range. The file has {total_lines} lines."

        end_line = min(start_line + limit, total_lines)
        displayed_content = ''.join([f'{i+start_line}\t{l}' for i, l in enumerate(contents[start_line - 1:end_line])])  # Adjust for 0-based index
        
        result = f"Displaying lines {start_line}-{end_line} of '{location}':\n\n"
        result += displayed_content

        if end_line < total_lines:
            result += "\n\n[Only showing " + str(limit) + " lines for readability...]"

        return result.strip()
    
    except Exception as e:
        return f"Error reading file '{location}': {e}"

def create_folder(
    location: Annotated[str, ..., "Folder path to create"]
) -> str:
    """
    Create a new folder at the specified location.

    Args:
        location: The folder path to be created.

    Returns:
        String message indicating success or error.
        Success and error messages are printed accordingly.
    """
    try:
        os.makedirs(location, exist_ok=True)
        msg = f"Folder '{location}' created successfully (or already exists)."
        print(msg)
        return msg
    except Exception as e:
        msg = f"Error creating folder '{location}': {e}"
        print(msg)
        return msg

def create_file(
    location: Annotated[str, ..., "File path to create"],
    content: Annotated[str, ..., "Content to be written into the new file"]
) -> str:
    """
    Create a new file at the specified location with the provided content.

    Args:
        location: File path for the new file.
        content: Content to write into the file.

    Returns:
        String message indicating success or error.
        All operations report success or error messages.
    """
    try:
        with open(location, 'w', encoding='utf-8') as f:
            f.write(content)
        msg = f"File '{location}' created successfully."
        return msg
    except Exception as e:
        msg = f"Error creating file '{location}': {e}"
        return msg

def run_bash(
    script: Annotated[str, ..., "Bash script code to execute"]
) -> str:
    """
    Execute a bash script provided as a string.

    Args:
        script: Bash script code as a string.

    Returns:
        Combined execution output/error message as a string.
        In case of an execution error, the error message is returned.
        If the code is wrapped in a code block, this function will extract the main code and run it.
    """
    try:
        process = subprocess.run(
            script, shell=True, text=True, capture_output=True, executable="/bin/bash"
        )
        output = process.stdout + process.stderr
        msg = f"Bash script executed successfully. Output:\n{output}"
        return msg
    except:
        try:
            process = subprocess.run(
                extract_code_from_block(script), shell=True, text=True, capture_output=True, executable="/bin/bash"
            )
            output = process.stdout + process.stderr
            msg = f"Bash script executed successfully. Output:\n{output}"
            return msg
        except Exception as e:
            error_msg = f"Error running bash script: {e}"
            return error_msg

def run_python(
    script: Annotated[str, ..., "Python script code to execute"]
) -> str:
    """
    Execute a Python script provided as a string.

    Args:
        script: Python script code as a string.

    Returns:
        Combined execution output/error message as a string.
        In case of an execution error, the error message is returned.
        If the code is wrapped in a code block, this function will extract the main code and run it.
    """
    try:
        process = subprocess.run(
            ["python", "-c", script],
            text=True, capture_output=True
        )
        output = process.stdout + process.stderr
        msg = f"Python script executed successfully. Output:\n{output}"
        return msg
    except:
        try:
            process = subprocess.run(
                ["python", "-c", extract_code_from_block(script)],
                text=True, capture_output=True
            )
            output = process.stdout + process.stderr
            msg = f"Python script executed successfully. Output:\n{output}"
            return msg
        except Exception as e:
            error_msg = f"Error running Python script: {e}"
            return error_msg
    
def list_dir(
    root: Annotated[str, ..., "Root folder path to list files and folders"]
):
    """
    List all files, folder given a root dirrectory

    Args:
        root: Root folder path to list files and folders

    Returns:
        A list of files, folders in the root dirrectory
    """
    try:
        objects = os.listdir(root)
        if len(objects) > 30:
            return 'Too many items in this folder, only display 30 items:\n' + "\n".join(objects) + '\n'
        return 'Found {} items in this folder:'.format(len(objects)) + '\n' + "\n".join(objects) + '\n'
    except Exception as e:
        return 'Encounter error:\n' + str(e)

def summarize_python_file(
    file_path: Annotated[str, ..., "Path to the Python file to analyze"]
) -> str:
    """
    Summarizes a Python file by listing all classes and functions with their arguments. Use this tool to summarize large files.

    Args:
        file_path: Path to the Python file to analyze

    Returns:
        Formatted string containing classes and functions, their arguments, and also the functions, classes being called inside.
        Success message with structured summary or error message.
    """
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        tree = ast.parse(code)
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error parsing file: {e}"

    analyzer = Analyzer()
    analyzer.visit(tree)

    output = []

    if analyzer.summary['classes']:
        output.append("Classes:")
        for cls in analyzer.summary['classes']:
            output.append(f"- {cls['name']} (line {cls['line']})")
            if cls['methods']:
                output.append("    Methods:")
                for method in cls['methods']:
                    method_name = method['name'].split('.')[-1]
                    args_str = ", ".join(method['args'])
                    calls = method['calls']
                    calls_str = ", ".join(calls) if calls else "None"
                    output.append(f"        {method_name} (line {method['line']}): arguments: ({args_str}), calls: [{calls_str}]")

    if analyzer.summary['functions']:
        output.append("\nFunctions:" if output else "Functions:")
        for func in analyzer.summary['functions']:
            args_str = ", ".join(func['args'])
            calls = func['calls']
            calls_str = ", ".join(calls) if calls else "None"
            output.append(f"- {func['name']} (line {func['line']}): arguments: ({args_str}), calls: [{calls_str}]")

    return "\n".join(output) if output else "No classes or functions found."

def check_pylint_errors(
    file_path: Annotated[str, ..., "Path to the Python file to check with pylint"]
) -> str:
    """
    Run pylint on the given Python file and return only error messages.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        A formatted string containing pylint error messages.
        If there are no errors, a message indicating this is returned.
        If an error occurs while running pylint, the error message is returned.
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: The file '{file_path}' does not exist."

        if not os.path.isfile(file_path):
            return f"Error: '{file_path}' is not a valid file."

        process = subprocess.run(
            ["pylint", "--errors-only", file_path],
            text=True, capture_output=True
        )

        pylint_output = process.stdout.strip()
        
        if not pylint_output:
            return f"No errors found in '{file_path}'."
        
        return f"Pylint errors in '{file_path}':\n\n{pylint_output}"

    except Exception as e:
        return f"Error running pylint on '{file_path}': {e}"

# NOT A TOOL
def extract_code_from_block(text: str) -> str:
    """
    Extracts the code from a code block formatted with triple backticks or triple tildes.
    
    Parameters:
        text (str): The input text containing the code block.
    
    Returns:
        str: Extracted code, or an empty string if no code block is found.
    """
    match = re.search(r"```(?:[a-zA-Z0-9]+)?\n(.*?)\n```|~~~(?:[a-zA-Z0-9]+)?\n(.*?)\n~~~", text, re.DOTALL)
    
    if match:
        return match.group(1) or match.group(2)  # Extract code from either backticks or tildes
    
    return text  # Return empty string if no match is found

def generate_success_message(location, new_lines, original_line_index, code_lines_length, mode, operation):
    if mode == 'replace':
        context_start = max(0, original_line_index - 8)
        context_end = min(len(new_lines), original_line_index + code_lines_length + 8)
        edit_start = original_line_index + 1
        edit_end = edit_start + code_lines_length - 1
        edit_range = range(edit_start, edit_end + 1)
    elif mode == 'insert':
        context_start = max(0, original_line_index - 8)
        context_end = min(len(new_lines), original_line_index + code_lines_length + 8)
        edit_start = (original_line_index + 1) + 1
        edit_end = edit_start + code_lines_length - 1
        edit_range = range(edit_start, edit_end + 1)
    elif mode == 'delete':
        context_start = max(0, original_line_index - 8)
        context_end = min(len(new_lines), original_line_index + 8)
        edit_range = []
    else:
        return f"Error: Invalid mode '{mode}'."

    context_lines = new_lines[context_start:context_end]
    context_str = []
    for i in range(context_start + 1, context_start + len(context_lines) + 1):
        line = new_lines[i - 1]
        prefix = '    '
        if i in edit_range:
            if mode == 'replace':
                prefix = '+-  '
            elif mode == 'insert':
                prefix = '++  '
        context_str.append(f"{i:4}{prefix}{line}")

    context_str = "\n".join(context_str)
    if location.endswith('.py'):
        context_str += ('\n' + check_pylint_errors(location))
    return (f"Successfully edited '{location}'\n"
            f"{operation}\n"
            f"Content after editing (lines {context_start + 1}-{context_end}):\n{context_str}")
##########################################

def replace_text(
    location: Annotated[str, ..., "File path to edit"],
    start_line: Annotated[int, ..., "Start line number to replace (1-based)"],
    end_line: Annotated[int, ..., "End line number to replace (1-based)"],
    code: Annotated[str, ..., "Code to replace the specified line range"]
) -> str:
    '''
    Replaces a specified range of lines in a file with the given code. Note that contents at `start_line` and `end_line` will also be replaced.

    Args:
        location (str): File path to edit.
        start_line (int): Start line number (1-based) of the range to replace.
        end_line (int): End line number (1-based) of the range to replace.
        code (str): New code to insert in place of the specified line range.

    Returns:
        On success, includes newly replaced lines with surrounding context.
        On error, returns descriptive error message.
    '''
    try:
        start_line = int(start_line)
        end_line = int(end_line)

        if not os.path.exists(location):
            return f"Error: File '{location}' does not exist."

        with open(location, 'r', encoding='utf-8') as f:
            original_lines = f.read().split('\n')

        if start_line < 1 or end_line < 1 or start_line > len(original_lines) or end_line > len(original_lines):
            return f"Error: Line numbers out of range (1-{len(original_lines)})"
        if start_line > end_line:
            return f"Error: Start line {start_line} is greater than end line {end_line}."

        start_idx = start_line - 1
        end_idx = end_line - 1
        code_lines = code.split('\n')

        new_lines = original_lines[:start_idx] + code_lines + original_lines[end_idx + 1:]

        with open(location, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        operation = f"Replaced lines {start_line}-{end_line} with {len(code_lines)} line(s)"
        return generate_success_message(
            location=location,
            new_lines=new_lines,
            original_line_index=start_idx,
            code_lines_length=len(code_lines),
            mode='replace',
            operation=operation
        )

    except Exception as e:
        return f"Error editing file '{location}': {e}"

def insert_text(
    location: Annotated[str, ..., "File path to edit"],
    line_number: Annotated[int, ..., "Line number to insert after (1-based)"],
    code: Annotated[str, ..., "Code to insert"]
) -> str:
    """
    Inserts the given code after a specified line number in a file.

    Args:
        location (str): File path to edit.
        line_number (int): Line number (1-based) after which the code should be inserted.
        code (str): The code to be inserted.

    Returns:
        On success, includes newly inserted lines with surrounding context.
        On error, returns descriptive error message.
    """
    try:
        line_number = int(line_number)

        if not os.path.exists(location):
            return f"Error: File '{location}' does not exist."

        with open(location, 'r', encoding='utf-8') as f:
            original_lines = f.read().split('\n')

        if line_number < 1 or line_number > len(original_lines):
            return f"Error: Line number {line_number} out of range (1-{len(original_lines)})"

        line_idx = line_number - 1
        code_lines = code.split('\n')

        new_lines = original_lines[:line_idx + 1] + code_lines + original_lines[line_idx + 1:]

        with open(location, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        operation = f"Inserted {len(code_lines)} line(s) after line {line_number}"
        return generate_success_message(
            location=location,
            new_lines=new_lines,
            original_line_index=line_idx,
            code_lines_length=len(code_lines),
            mode='insert',
            operation=operation
        )

    except Exception as e:
        return f"Error editing file '{location}': {e}"

def remove_text(
    location: Annotated[str, ..., "File path to edit"],
    start_line: Annotated[int, ..., "Start line number to remove (1-based)"],
    end_line: Annotated[int, ..., "End line number to remove (1-based)"]
) -> str:
    """
    Removes a specified range of lines from a file. Note that contents at line `start_line` and `end_line` will also be removed

    Args:
        location (str): File path to edit.
        start_line (int): Start line number (1-based) to remove.
        end_line (int): End line number (1-based) to remove.

    Returns:
        On success, includes content of the file around the removed position
        On error, returns descriptive error message.
    """
    try:
        start_line = int(start_line)
        end_line = int(end_line)

        if not os.path.exists(location):
            return f"Error: File '{location}' does not exist."

        with open(location, 'r', encoding='utf-8') as f:
            original_lines = f.read().split('\n')

        if start_line < 1 or end_line < 1 or start_line > len(original_lines) or end_line > len(original_lines):
            return f"Error: Line numbers out of range (1-{len(original_lines)})"
        if start_line > end_line:
            return f"Error: Start line {start_line} is greater than end line {end_line}."

        start_idx = start_line - 1
        end_idx = end_line - 1

        new_lines = original_lines[:start_idx] + original_lines[end_idx + 1:]

        with open(location, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        operation = f"Deleted lines {start_line}-{end_line}"
        return generate_success_message(
            location=location,
            new_lines=new_lines,
            original_line_index=start_idx,
            code_lines_length=0,
            mode='delete',
            operation=operation
        )

    except Exception as e:
        return f"Error editing file '{location}': {e}"

def remove_file_or_dir(
    path: Annotated[str, ..., "Path to the file or folder to remove"]
) -> str:
    """
    Remove a file or directory at the specified path
    
    Args:
        path: Path to the file/folder to be removed. 
              Can be either relative or absolute path
        
    Returns:
        Success message or error description
    """
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f"Successfully removed file: {path}"
        elif os.path.isdir(path):
            shutil.rmtree(path)  # Handles directories with content
            return f"Successfully removed directory: {path}"
        return f"Path not found: {path}"
    except Exception as e:
        return f'Error removing {path}:\n{str(e)}'

def rename_file_or_dir(
    source: Annotated[str, ..., "Current path of the file or folder"],
    destination: Annotated[str, ..., "New path for the file or folder"]
) -> str:
    """
    Rename or move a file/directory from source to destination
    
    Args:
        source: Current path of the item to rename
        destination: New path for the item
        
    Returns:
        Success message or error description
    """
    try:
        os.rename(source, destination)
        return f"Successfully renamed '{source}' to '{destination}'"
    except Exception as e:
        return f'Error renaming {source} to {destination}:\n{str(e)}'

def apply_patch(
    diff_text: Annotated[str, ..., "Patch/diff content to apply"],
    project_root: Annotated[str, ..., "Path to GitHub project root directory"]
) -> str:
    """
    Apply a unified diff patch to a local Git repository. Valid unified diff text containing:
    - File paths relative to project root
    - Correct line numbers
    - Context lines for accurate patching
    
    Args:
        diff_text: Unified diff/patch content to apply
        project_root: Root directory of the GitHub project
        
    Returns:
        Success message or error description
    """
    try:
        # Validate project root exists
        if not os.path.isdir(project_root):
            return f"Project directory not found: {project_root}"
        
        # Ensure project_root is a Git repository
        if not os.path.isdir(os.path.join(project_root, ".git")):
            return "Error: The specified directory is not a Git repository."
        
        # Create temporary patch file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as patch_file:
            patch_file.write(diff_text)
            patch_file.flush()  # Ensure all data is written
            patch_path = patch_file.name
        
        try:
            # Apply patch using git apply
            result = subprocess.run(
                ['git', 'apply', '--whitespace=fix', patch_path],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return f"Patch failed:\n{result.stderr.strip()}"
            
            return "Patch applied successfully!"
        finally:
            os.remove(patch_path)  # Cleanup temporary file
        
    except Exception as e:
        return f"Error applying patch:\n{str(e)}"

