from typing import Any, Dict, Tuple
from ..chatbot.base import *
import inspect

class ThinkMeta(type):
    def __mul__(cls, other):
        return ChainedProcessor(cls(), other())
    
    def __getitem__(cls, conditions):
        return RepeatedProcessor(cls(), conditions)

class ThinkProcessor(metaclass=ThinkMeta):
    modifies: Tuple[str] = ()
    def __init__(self):
        self.requires = tuple(inspect.signature(self.process).parameters)

    def inp(self, *requires):
        self.requires = requires
        return self
    
    def out(self, *modifies):
        self.modifies = modifies
        return self
    
    def __call__(self, query: Dict) -> Dict:
        try:
            inputs = [query[k] for k in self.requires]
        except AttributeError as e:
            raise MissingFieldError(f"Missing required field: {e}")
        
        outputs = {modify: answer for modify, answer in zip(self.modifies, self.process(*inputs))}
        query.update(**outputs)
        return query
    
    def process(self, *args) -> Dict[str, Any]:
        raise NotImplementedError
    
    def __mul__(self, other):
        return ChainedProcessor(self, other)
    
    def __getitem__(self, conditions):
        return RepeatedProcessor(self, conditions)
    
    def chat(self, **kwargs):
        return self.__call__(kwargs)['answer']

class ChainedProcessor(ThinkProcessor):
    def __init__(self, *processors):
        self.processors = processors
        
    def process(self, *args):
        raise NotImplementedError("ChainedProcessor should use __call__ directly")
    
    def __call__(self, query: Dict) -> Dict:
        for processor in self.processors:
            query = processor(query)
        return query

class RepeatedProcessor(ThinkProcessor):
    def __init__(self, processor, conditions):
        self.processor = processor
        self.conditions = self._parse_conditions(conditions)
        
    def _parse_conditions(self, conditions):
        if not isinstance(conditions, tuple):
            conditions = (conditions,)
        
        parsed = {'max_repeats': 1000, 'until': []}
        for item in conditions:
            if isinstance(item, int):
                parsed['max_repeats'] = item
            elif callable(item):
                parsed['until'].append(item)
        return parsed
    
    def __call__(self, query: Dict) -> Dict:
        for _ in range(self.conditions['max_repeats']):
            query = self.processor(query)
            if all(cond(query) for cond in self.conditions['until']):
                break
        return query

class TextProcessor(ThinkProcessor):
    modifies = ('answer',)
    
    def __init__(self, chatbot, template):
        super().__init__()
        self.chatbot = chatbot
        self.template = template
        
    def process(self, query) -> Dict[str, Any]: return (self.chatbot(self.template.format(query=query)), )

class ChatProcessor(ThinkProcessor):
    modifies = ('answer', 'history', )

    def __init__(self, chatbot):
        super().__init__()
        self.chatbot = chatbot

    def process(self, query, history: History) -> Dict[str, Any]:
        history.user(query)
        answer = self.chatbot(history)
        history.ai(answer)
        return (answer, history)

class MissingFieldError(Exception):
    pass