from .base import ThinkProcessor
    
class ListMemoryProcessor(ThinkProcessor):
    modifies = ('memory',)

    def __init__(self):
        super().__init__()
    
    def process(self, memory, state):
        if isinstance(memory, list): memory.append(state)
        else: memory = [state]
        return (memory, )
