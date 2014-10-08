import levelgen
import entity


class GameInstance(object):
    def __init__(self, state):
        self.state = state

        self.observers = []

    def notify(self, name, *args, **kwargs):
        for o in self.observers:
            o.notify(name, *args, **kwargs)


class GameInstanceState(object):
    def __init__(self, levels):
        self.current_level = 0
        self.levels = levels[:]

    def get_current_level(self):
        return self.levels[self.current_level]


class Map:
    def __init__(self, data):
        self.size = len(data[0]), len(data)
        self.data = data

    def get_tile(self, x, y):
        return self.data[y][x]

    def console_print(self):
        for row in self.data:
            print [str(tile) for tile in row]


class Tile(object):
    def __init__(self, type):
        self.type = type

    @property
    def passable(self):
        return self.type.passable

    def __str__(self):
        return self.type.char


class TileType:
    def __init__(self, name, char, passable):
        self.name = name
        self.char = char
        self.passable = passable


class Level:
    def __init__(self, map, rooms):
        self.map = map
        self.rooms = rooms

        self.init()

    def init(self):
        map = self.map

        for room in self.rooms:
            room.level = self

            room_padded_area = room.padded_area
            room_entrances = set()
            for x in xrange(room_padded_area.left, room_padded_area.right):
                y = room_padded_area.top
                if map.get_tile(x, y).passable:
                    room_entrances.add((x, y))

                y = room_padded_area.bottom - 1
                if map.get_tile(x, y).passable:
                    room_entrances.add((x, y))

            for y in xrange(room_padded_area.top, room_padded_area.bottom):
                x = room_padded_area.left
                if map.get_tile(x, y).passable:
                    room_entrances.add((x, y))

                x = room_padded_area.right - 1
                if map.get_tile(x, y).passable:
                    room_entrances.add((x, y))

            room.entry_points = list(room_entrances)


tile_type_wall = TileType('wall', '#', False)
tile_type_floor = TileType('floor', ' ', True)

def gen_level(size):
    gen_info = levelgen.generate((60, 60))

    map_data = gen_info.passability_map
    for y in xrange(60):
        for x in xrange(60):
            if map_data[y][x]:
                map_data[y][x] = Tile(tile_type_floor)
            else:
                map_data[y][x] = Tile(tile_type_wall)
    map = Map(map_data)

    rooms = []
    for room_area in gen_info.room_areas:
        rooms.append(entity.Room(room_area))

    level = Level(map, rooms)
    return level


def gen_map(size):
    data = []
    for y in xrange(size[1]):
        row = []
        for x in xrange(size[0]):
            row.append(Tile(tile_type_wall))
        data.append(row)

    data[1][1] = Tile(tile_type_floor)

    return Map(data)


instance = None


def new():
    levels = [gen_level((50, 50))]

    state = GameInstanceState(levels)

    global instance
    instance = GameInstance(state)


