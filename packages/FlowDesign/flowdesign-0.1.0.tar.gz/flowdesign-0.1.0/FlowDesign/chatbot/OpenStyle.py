from openai import OpenAI
from .base import *

class OpenAIStyle(Chatbot):
    def __init__(self, api_key, model_name='deepseek/deepseek-v3-base:free', base_url='https://openrouter.ai/api/v1', **kwargs):
        super().__init__(None)
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model_name = model_name
        self.kwargs = kwargs
        self.mapper = {'ai': 'assistant', 'user': 'user', 'system': 'system', 'human': 'user', 'bot': 'assistant', 'agent': 'assistant'}

    def __run_one_sample(self, user_input):
        completion = self.client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model=self.model_name,
            messages=[{ 'role': 'user', 'content': user_input }]
            if isinstance(user_input, str) else 
            [{'role': self.mapper[i.type], 'content': i.content} for i in user_input],
            **self.kwargs
        )

        return completion.choices[0].message.content

    def run(self, user_input, batch=False):
        if batch:
            return [self.__run_one_sample(i) for i in user_input]
        return self.__run_one_sample(user_input)