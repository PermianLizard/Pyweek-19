

class Room(object):
    def __init__(self, area):
        self.area = area
        self.level = None
        self.entry_points = None

    @property
    def padded_area(self):
        return self.area.inflate(2, 2)


class Being(object):
    def __init__(self, pos=(0, 0)):
        self.pos = pos