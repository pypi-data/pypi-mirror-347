from .base import ThinkProcessor
from duckduckgo_search import DDGS

class DDGSearchProcessor(ThinkProcessor):
    modifies = ('answer', )

    def __init__(self, chatbot, ddg_method='text'):
        super().__init__()
        self.chatbot = chatbot
        method_list = {
            'text': DDGS().text,
            'answers': DDGS().answers,
            'video': DDGS().videos,
            'news': DDGS().news,
            'images': DDGS().images,
            'chat': DDGS().chat,
            'maps': DDGS().maps,
            'translate': DDGS().translate,
            'suggestions': DDGS().suggestions
        }
        self.ddg_method = method_list[ddg_method]
    
    def process(self, query):
        return (self.ddg_method(query), )