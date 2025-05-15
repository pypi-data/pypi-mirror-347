from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from typing import List
from ..utils.pattern import Batcher
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_huggingface import HuggingFaceEndpoint, HuggingFacePipeline
from ..utils import cache
import base64, os
from io import BytesIO
from PIL import Image
from typing import Tuple
# from langchain_community.llms import VLLM

def get_image_data(content):
    if isinstance(content, Image.Image):
        with BytesIO() as buffer:
            content.save(buffer, format="JPEG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
    elif isinstance(content, str) and os.path.exists(content):
        with open(content, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
    else:
        return {"type": "text", "text": content}

    return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}

# MAIN
class History(List):
    def user(self, contents):
        if isinstance(contents, tuple): contents = [get_image_data(content) for content in contents]
        self.append(HumanMessage(content=contents))
    def ai(self, content): self.append(AIMessage(content=content))
    def system(self, content): self.append(SystemMessage(content=content))

class Chatbot(Batcher):
    def __init__(self, chat_model: BaseChatModel):
        super().__init__()
        self.chat_model = chat_model
        self.tools = []

    def set_tools(self, tools):
        self.tools = tools

    def run(self, user_input, batch=False):
        if batch: # batch handle
            if self.tools:
                return [(i.content, i.tool_calls)
                        for i in self.chat_model.bind_tools(self.tools).batch(user_input)]

            return [i if isinstance(i, str)
                    else getattr(i, 'content', None)
                    for i in self.chat_model.batch(user_input)]

        # One sample handle
        if self.tools:
            response = self.chat_model.bind_tools(self.tools).invoke(user_input)
            return (response.content, response.tool_calls)
        
        response = self.chat_model.invoke(user_input)
        return response if isinstance(response, str) else getattr(response, 'content', None)

class ChatGPTbot(Chatbot):
    def __init__(self, api_token, model_name='gpt-4o-mini', **kwargs):
        super().__init__(ChatOpenAI(
            model_name=model_name,
            api_key=api_token,
            **kwargs
            ))

class GeminiBot(Chatbot):
    def __init__(self, api_token, model_name='gemini-1.5-flash', **kwargs):
        super().__init__(ChatGoogleGenerativeAI(
            model=model_name,
            api_key=api_token,
            **kwargs
        ))

class HuggingFacebot(Chatbot):
    def __init__(self, api_token,
                 model_repo_id='meta-llama/Llama-3.2-3B-Instruct',
                 run_local=False, prompt_template='{history}ai:\n',
                 **kwargs):
        '''
        run_local:
            - hg: use huggingface
            - ol: use ollama
        '''

        if run_local == 'hg':
            llm = HuggingFacePipeline.from_model_id(
                model_id=model_repo_id,
                task='text-generation',
                # model_kwargs={'padding_side': 'left'},
                **kwargs
            )
        elif run_local == 'ol':
            llm = OllamaLLM(model=model_repo_id)
        else:
            llm = HuggingFaceEndpoint(
                repo_id=model_repo_id,
                huggingfacehub_api_token=api_token,
                **kwargs
            )

        super().__init__(PromptTemplate.from_template(template=prompt_template) | llm)

    def format_history(self, history: List[BaseMessage]):
        return ''.join([f"{message.type}:\n{message.content}\n" for message in history])

    def filtering(self, answer): return answer

    def __prerun(self, user_input):
        if isinstance(user_input, str): user_input = [HumanMessage(content=user_input)]
        return {'history': self.format_history(user_input)}

    def __postrun(self, response):
        return self.filtering(response if isinstance(response, str) else getattr(response, 'content', None))

    def run(self, user_input: str, batch=False):
        if batch:
            responses = self.chat_model.batch([self.__prerun(i) for i in user_input])
            return [self.__postrun(i) for i in responses]

        user_input = self.__prerun(user_input)
        return self.__postrun(self.chat_model.invoke(user_input))
