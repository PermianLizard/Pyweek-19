class Player:
    def __init__(self, colors, is_human=False):
        self.level = None
        self.dark_color, self.color, self.light_color = colors
        self.is_human = True