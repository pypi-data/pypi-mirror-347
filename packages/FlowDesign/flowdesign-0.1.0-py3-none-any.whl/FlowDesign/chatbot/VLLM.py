from .base import *
from langchain_community.llms import VLLM

class VLLMbot(Chatbot):
    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct",
        trust_remote_code=True,  # mandatory for hf models
        max_new_tokens=128,
        top_k=10,
        top_p=0.95,
        temperature=0.8,
        dtype='half',
        max_model_len=512,
        **kwargs):
        super().__init__(None)
        self.client = VLLM(model=model_name,
                           trust_remote_code=trust_remote_code,
                           max_new_tokens=max_new_tokens,
                           top_k=top_k,
                           top_p=top_p,
                           temperature=temperature,
                           dtype=dtype,
                           max_model_len=max_model_len,
                           **kwargs)
        self.model_name = model_name
        self.kwargs = kwargs

    def run(self, user_input, batch=False):
        if batch:
            return self.client.batch([i for i in user_input])
        return self.client.invoke(user_input)