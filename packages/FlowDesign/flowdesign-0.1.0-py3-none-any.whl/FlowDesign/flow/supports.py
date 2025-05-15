from ..processor import *
import inspect, re
from typing_extensions import TypedDict
from typing import Callable

def extract_function_calls(text):
    pattern = re.compile(r'<function.(.*?)>(.*?)</function>', re.DOTALL)
    param_pattern = re.compile(r'<parameter.(.*?)>(.*?)</parameter>', re.DOTALL)
    
    functions = []
    for match in pattern.finditer(text):
        func_name = match.group(1)
        params = {p.group(1): p.group(2) for p in param_pattern.finditer(match.group(2))}
        functions.append({'name': func_name, 'args': params})
    
    return functions

def truncate_history(history: History, max_limit):
    if len(history) > max_limit:
        return History(
            [history[0]] + history[-max_limit:]
        )
    return history

def get_tool_description(tools, template):
    return '\n'.join([template.format(
            name=i.__name__,
            parameters='(' + ', '.join([f'{v}' for k, v in inspect.signature(i).parameters.items() if k not in ('kwargs', 'args')]) + ')',
            description=i.__doc__) for i in tools])

def get_tool_list_for_supported_agents(tools: List[Callable]):
    """Convert a function with Annotated parameters to a TypedDict."""
    results = []
    for func in tools:
        v = {k:v.annotation for k,v in inspect.signature(func).parameters.items()}
        result = TypedDict(func.__name__, v)
        result.__doc__ = func.__doc__
        results.append(result)
    return results