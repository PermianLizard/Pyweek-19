from core import color
import levelgen
import entity
import player


class Level:
    def __init__(self, map, players, rooms, beings):
        self.map = map
        self.players = []
        self.rooms = []
        self.beings = []

        for player in players:
            self.add_player(player)

        for room in rooms:
            self.add_room(room)

        for being in beings:
            self.add_being(being)

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

    def update(self):
        for room in self.rooms:
            room.update()

        for being in self.beings:
            being.update()

    def add_player(self, player):
        self.players.append(player)
        player.level = self

    def add_room(self, room):
        self.rooms.append(room)
        room.level = self

    def add_being(self, being):
        self.beings.append(being)
        being.level = self

    def get_beings_at(self, x, y):
        pos = (x, y)
        return [being for being in self.beings if being.pos == pos]

    def filter_passable(self, pos_list):
        map_passable_list = self.map.filter_passable(pos_list)
        return [pos for pos in map_passable_list if len(self.get_beings_at(*pos)) == 0]


class Map:
    def __init__(self, data):
        self.size = len(data[0]), len(data)
        self.data = data
        self.passability_data = self._gen_passability_data()

    def get_tile(self, x, y):
        return self.data[y][x]

    def get_passable(self, x, y):
        return self.passability_data[y][x]

    def console_print(self):
        for row in self.data:
            print [str(tile) for tile in row]

    def filter_passable(self, pos_list):
        return (pos for pos in pos_list if self.get_passable(*pos))

    def _gen_passability_data(self):
        passability_data = []
        data = self.data
        for y in xrange(len(data)):
            row = []
            for x in xrange(len(data[y])):
                row.append(data[y][x].passable)
            passability_data.append(row)

        return passability_data


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


tile_type_wall = TileType('wall', '#', False)
tile_type_floor = TileType('floor', ' ', True)


def gen_level(size, seed=None):
    width, height = size
    gen_info = levelgen.generate(size, seed=seed)

    map_data = gen_info.passability_map
    for y in xrange(height):
        for x in xrange(width):
            if map_data[y][x]:
                map_data[y][x] = Tile(tile_type_floor)
            else:
                map_data[y][x] = Tile(tile_type_wall)
    map = Map(map_data)

    independent_player = player.Player((color.DARK_GRAY, color.GRAY, color.SILVER))
    human_player = player.Player((color.DARK_RED, color.RED, color.LIGHT_RED))
    players = [independent_player, human_player]

    rooms = []
    for room_area in gen_info.room_areas:
        rooms.append(entity.Room(room_area, independent_player))

    first_room = rooms[0]

    beings = []
    beings.append(entity.Being(90, first_room.area.center, human_player))
    beings.append(entity.Being(90, first_room.area.move(-1, -1).center, human_player))
    beings.append(entity.Being(90, first_room.area.move(1, 1).center, human_player))
    beings.append(entity.Being(90, first_room.area.move(-1, 1).center, human_player))
    beings.append(entity.Being(90, first_room.area.move(1, -1).center, human_player))

    level = Level(map, players, rooms, beings)
    return level
