from ..processor import *

class PALFlow(ThinkProcessor):
    modifies = ('answer', )

    def __init__(self, chatbot):
        nlp = TextProcessor(chatbot, 'Write a executable Python program to solve the problem: {query}')
        exec = PythonProcessor().inp('answer').out('answer')
        self.flow = nlp*exec # ask llm to gen code -> exec code

    def __call__(self, query):
        return self.flow(query)