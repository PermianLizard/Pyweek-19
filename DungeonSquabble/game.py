class GameInstance(object):
    def __init__(self, state):
        self.state = state

        self.observers = []

    def notify(self, name, *args, **kwargs):
        for o in self.observers:
            o.notify(name, *args, **kwargs)


class GameInstanceState(object):
    def __init__(self):
        self.current_level = 0
        self.levels = []


class Map:
    def __init__(self, data):
        self.data = data

    def console_print(self):
        for row in self.data:
            print [str(tile) for tile in row]


class Tile(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type.char


class TileType:
    def __init__(self, name, char):
        self.name = name
        self.char = char


class Level:
    def __init__(self, map):
        self.map = map


tile_type_wall = TileType('wall', '#')
tile_type_floor = TileType('floor', ' ')

instance = None


def new():
    state = GameInstanceState()

    global instance
    instance = GameInstance(state)


def gen_level(size):
    level = Level(None)

    return level


def gen_map(size):
    data = []
    for y in xrange(size[1]):
        row = []
        for x in xrange(size[0]):
            row.append(Tile(tile_type_wall))
        data.append(row)

    return Map(data)


if __name__ == '__main__':
    m = gen_map((5, 5))
    m.console_print()