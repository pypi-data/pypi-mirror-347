from .base import *
from langchain_ollama.llms import OllamaLLM

class Ollama(Chatbot):
    def __init__(self, model_name="deepseek-r1:1.5b", **kwargs):
        super().__init__(None)
        self.client = OllamaLLM(model=model_name)
        self.model_name = model_name
        self.kwargs = kwargs

    def run(self, user_input, batch=False):
        if batch:
            return self.client.batch([i for i in user_input])
        return self.client.invoke(user_input)