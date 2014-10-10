class Player:
    def __init__(self, name, colors, is_human=False):
        self.level = None
        self.name = name
        self.dark_color, self.color, self.light_color = colors
        self.is_human = True
        self.rooms = []

    def init(self):
        pass

    def add_room(self, room):
        self.rooms.append(room)
        room.owner = self