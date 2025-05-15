from .base import ThinkProcessor
import subprocess
from typing import Dict
import re

def python_code(markdown_text):
    """Extracts Python code blocks, wraps them in try-except, and merges them."""
    pattern = r"```python\n(.*?)\n```"
    matches = re.findall(pattern, markdown_text, re.DOTALL)
    
    wrapped_code = []
    for idx, code in enumerate(matches, 1):
        wrapped_code.append(f"try:\n" + "\n".join(f"    {line}" for line in code.split("\n")) + f"\nexcept Exception as e:\n    print(f'Error in block {idx}:', e)\n")

    return "\n".join(wrapped_code)

class PythonProcessor(ThinkProcessor):
    modifies = ('program_output', 'program_error', )

    def __init__(self, code_wrap='{code}', pwd='.'):
        super().__init__()
        self.code_wrap = code_wrap
        self.pwd = pwd

    def process(self, code) -> Dict:
        result = subprocess.run(["python3", "-c", self.code_wrap.format(code=python_code(code))],
                                cwd=self.pwd, capture_output=True, text=True)
        return (result.stdout, result.stderr, )

class CommandProcessor(ThinkProcessor):
    modifies = ('stdout', 'stderr', )

    def __init__(self, command='pwd', pwd='.'):
        super().__init__()
        self.command, self.pwd = command, pwd

    def process(self):
        output = subprocess.run([self.command], cwd=self.pwd, capture_output=True, text=True)
        return (output.stdout, output.stderr, )
