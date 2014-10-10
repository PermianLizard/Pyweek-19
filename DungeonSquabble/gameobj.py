from core import color
import levelgen
import entity
import player


class Level:
    def __init__(self, map, players, rooms):
        self.map = map
        self.players = []
        self.rooms = []
        self.beings = []
        self.human_player = None

        for player in players:
            self._add_player(player)
        for room in rooms:
            self._add_room(room)

    def init(self):
        for player in self.players:
            player.init()

        for room in self.rooms:
            room.init()

    def update(self):
        for room in self.rooms:
            room.update()

        for being in self.beings:
            being.update()

    def add_beings(self, beings):
        for being in beings:
            self.add_being(being)

    def add_being(self, being):
        self.beings.append(being)
        being.level = self
        being.init()

    def get_beings_owned_by(self, player):
        return [being for being in self.beings if being.owner == player]

    def get_beings_at(self, x, y):
        pos = (x, y)
        return [being for being in self.beings if being.pos == pos]

    def get_passable(self, x, y):
        map_pass = self.map.get_passable(x, y)
        if map_pass:
            return len(self.get_beings_at(x, y)) == 0
        return False

    def filter_passable(self, pos_list):
        return [pos for pos in pos_list if self.get_passable(*pos)]

    def _add_player(self, player):
        self.players.append(player)
        player.level = self
        if player.is_human:
            self.human_player = player

    def _add_room(self, room):
        self.rooms.append(room)
        room.level = self


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

    # create map data
    map_data = gen_info.passability_map
    for y in xrange(height):
        for x in xrange(width):
            if map_data[y][x]:
                map_data[y][x] = Tile(tile_type_floor)
            else:
                map_data[y][x] = Tile(tile_type_wall)
    map = Map(map_data)

    # create rooms
    rooms = []
    for room_area in gen_info.room_areas:
        rooms.append(entity.Room(room_area))

    # for each room, create indie player who owns that room
    players = []
    for room in rooms:
        indie_player = player.Player('Independents', (color.DARK_GRAY, color.GRAY, color.SILVER))
        indie_player.add_room(room)
        players.append(indie_player)

    human_player = player.Player('You', (color.DARK_RED, color.RED, color.LIGHT_RED), is_human=True)
    players.append(human_player)

    level = Level(map, players, rooms)
    level.init()

    # add beings
    beings = []

    first_room = level.rooms[0]
    beings.append(entity.Being(90, first_room.area.center, human_player))
    beings.append(entity.Being(90, first_room.area.move(-1, -1).center, human_player))
    beings.append(entity.Being(90, first_room.area.move(1, 1).center, human_player))
    beings.append(entity.Being(90, first_room.area.move(-1, 1).center, human_player))
    beings.append(entity.Being(90, first_room.area.move(1, -1).center, human_player))

    second_room = level.rooms[1]
    beings.append(entity.Being(90, second_room.area.center, second_room.owner))

    level.add_beings(beings)

    return level
