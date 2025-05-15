from .base import *

class ImBot(HuggingFacebot):
    '''
Example chat:
<|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>

<|im_start|>user
What is the weather like today in New York?<|im_end|>

<|im_start|>assistant
<tool_call>
{"name": "get_weather", "arguments": {"location": "New York"}}
</tool_call><|im_end|>
'''
    prompt_template='{history}<|im_start|>assistant\n'
    mapper = {'ai': 'assistant', 'human': 'user', 'system': 'system'}

    def __init__(self, api_token, model_repo_id='Qwen/Qwen2.5-0.5B-Instruct',
                 run_local='hg', **kwargs):
        super().__init__(api_token, model_repo_id, run_local, self.prompt_template, **kwargs)

    def filtering(self, answer):
        return answer.split('<|im_start|>assistant\n')[-1].split('</think>')[-1]

    def format_history(self, history):
        return ''.join([f"<|im_start|>{self.mapper[message.type]}\n{message.content}<|im_end|>\n" for message in history])
    