class AugmentedBar:
    def __init__(self, bar):
        self.bar = bar
        self.indicatos = {}

    def add_indicator(self, id, value):
        # assert no overwrite?
        self.indicatos[id] = value