# Design flow for LLM

## Example use

This framework can be used to create new flow easily, for example:
```python
from FlowDesign.processor import *

class PALFlow(ThinkProcessor):
    modifies = ('answer', )

    def __init__(self, chatbot):
        nlp = TextProcessor(chatbot, 'Write a executable Python program to solve the problem: {query}')
        exec = PythonProcessor().inp('answer').out('answer')
        self.flow = nlp*exec # ask llm to gen code -> exec code

    def __call__(self, query):
        return self.flow(query)
```

How to use the built-in PAL flow with gemini
```python
from FlowDesign.flow.pal import PALFlow
from FlowDesign.chatbot.base import GeminiBot

bot = GeminiBot('GEMINI_TOKEN')
flow = PALFlow(bot)
output1 = flow.chat('what is the result of (1231.23*3242.432^2)/7?+pi^(2^pi)-e^(pi^2)')
output2 = flow.chat('sort this list: [1,232,4,432,34,25,13,31,23,32,324,3,5,23,32,3,2,2,2,2,2,2,2,2,2,2,2,2]')
```
