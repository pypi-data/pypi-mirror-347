'''
Example how to implement tools, remember that input type of tools is always string without setting builtin_fnc_call to True.

```python
from typing_extensions import Annotated

def add(a: Annotated[int, ..., 'First int'], b: Annotated[int, ..., 'Second int']) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return f'Result of {a}+{b} is: ' + str(int(a) + int(b))


def multiply(a: Annotated[int, ..., 'First int'], b: Annotated[int, ..., 'Second int']) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return f'Result of {a}*{b} is: ' + str(int(a) * int(b))
```
'''

from .supports import *

class Agent(ThinkProcessor):
    SYSTEM_PROMPT_SUFFIX_TEMPLATE_FOR_NON_SUPPORTED_FNC_CALL = """\
You will chat with both USER, who give you task, problem, and ENVIRONMENT, which will give you the result of your function calling and remind you how many turns you have left to provide the final answer. Note that, when the task begin, you have {turn} turns to discover, understand, and provide the final answer. You have access to the following functions:

{description}

If you choose to call a function ONLY reply in the following format with NO suffix:

<function example_function_name>
<parameter example_parameter_1>value_1</parameter>
<parameter example_parameter_2>
This is the value for the second parameter
that can span
multiple lines
</parameter>
</function>

<IMPORTANT>
Reminder:
- Function calls MUST follow the specified format, start with <function and end with </function>.
- Required parameters MUST follow the specified format, start with <parameter example_parameter> and end with </parameter>.
- You can only call one function each turn.
- You may provide optional reasoning for your function call in natural language BEFORE the function call, but NOT after.
- If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls.
- DO NOT provide your information like time limit in the answer, this information is only known by you and ENVIRONMENT.

Note:
<function example_function>
<parameter example_parameter_1>value_1</parameter>
<parameter example_parameter_2>This is the value for the second parameter
that can span
multiple lines
</parameter>
</function>

is completely different from 

<function example_function>
<parameter example_parameter_1>value_1</parameter>
<parameter example_parameter_2>This is the value for the second parameter\\nthat only span\\none line</parameter>
</function>
"""

    TOOL_REPRESENTATION_TEMPLATE = 'Tool {name}{parameters}:\n{description}'

    SYSTEM_PROMPT_SUFFIX_TEMPLATE_FOR_SUPPORTED_FNC_CALL = """\
You will chat with both USER, who give you task, problem, and ENVIRONMENT, which will give you the result of your function calling and remind you how many turns you have left to provide the final answer. Note that, when the task begin, you have {turn} turns to discover, understand, and provide the final answer. You have access to the following functions:

When you think you have completed the task, you must provide a detailed final answer without calling any functions, tools. And you should not stop to try to solve the user's request only until the task is completed.

[IMPORTANT] You can only complete the task by coding. Talk is cheap, show me the code with tools.
"""

    modifies = ('answer', )

    def __init__(self,
                 chatbot: Chatbot,
                 prefix_prompt = '',
                 tools: List[Callable]=[],
                 repeat=5,
                 history_limit=7,
                 builtin_fnc_call=False,
                 max_env_response=2000):
        super().__init__()
        self.chatbot = chatbot
        self.repeat = repeat
        self.max_env_response = max_env_response
        self.history_limit = history_limit
        self.builtin_fnc_call = builtin_fnc_call
        self.history = History()
        self.tools = {i.__name__: i for i in tools}

        if builtin_fnc_call:
            tools = get_tool_list_for_supported_agents(tools)
            self.history.system(prefix_prompt + self.SYSTEM_PROMPT_SUFFIX_TEMPLATE_FOR_SUPPORTED_FNC_CALL.format(turn=repeat))
        else:
            description = get_tool_description(tools, self.TOOL_REPRESENTATION_TEMPLATE)
            self.history.system(prefix_prompt + self.SYSTEM_PROMPT_SUFFIX_TEMPLATE_FOR_NON_SUPPORTED_FNC_CALL.format(description=description, turn=repeat))

    def process(self, query):
        self.history.user(f'USER\n{query}')
        for i in range(self.repeat):
            self.history = truncate_history(self.history, self.history_limit)

            if self.builtin_fnc_call:
                self.chatbot.set_tools(self.tools.values())
                answer, functions = self.chatbot(self.history)
            else:
                answer = self.chatbot(self.history)
                functions = extract_function_calls(answer)

            print(answer)
            self.history.ai(answer)

            if functions == []:
                return (answer, )
            
            if i == (self.repeat - 1):
                break

            responses = []
            for func in functions:
                try:
                    response = self.tools[func['name']](**func['args'])
                except Exception as e:
                    response = str(e)
                # params = ', '.join([f'{k}="""{v}"""' for k,v in func['args'].items()])
                func_notation = f"{func['name']}"
                responses.append(f'Result of {func_notation}:\n{response}')

            responses = 'ENVIRONMENT\n' + '\n\n'.join(responses)
            if len(responses) > self.max_env_response:
                responses = responses[:self.max_env_response] + ' ...'
            response += f'\n\nYou have {self.repeat-i-1} turns left.'
            if (self.repeat-i) <= 2: responses += ' You must provide the final answer without calling function now.'

            print(responses)
            self.history.user(responses)

            print('* '*30)

        return ("TASK FAILED", )
    

