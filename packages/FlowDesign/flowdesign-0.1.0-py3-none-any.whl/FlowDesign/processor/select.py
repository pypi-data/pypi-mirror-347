from .base import ThinkProcessor

class MCProcessor(ThinkProcessor):
    modifies = ('select', 'scores', 'states', )

    def __init__(self):
        super().__init__()

    def process(self, scores, states):
        if len(states) != 0:
            best_score, best_state = max(zip(scores, states), key=lambda x: x[0])
            scores.remove(best_score)
            states.remove(best_state)
            return (best_state, scores, states, )
        return (None, None, None, )

class SelectProcessor(ThinkProcessor):
    modifies = ('answer', )

    def __init__(self, mapping: dict):
        super().__init__()
        self.mapping = mapping

    def process(self, options, answer):
        if options in self.mapping: return self.mapping[options](answer)
        return (None, )
