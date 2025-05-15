from .base import ThinkProcessor
import re

class ParseCodeProcessor(ThinkProcessor):
    requires = ('answer', )
    modifies = ('answer', )

    def __init__(self, text='{code}'):
        super().__init__()
        self.text = text

    def process(self, answer):
        match = re.search(r"```[\w]*\n(.*?)```", self.text.format(code=answer), re.DOTALL)
        return (match.group(1) if match else "", )