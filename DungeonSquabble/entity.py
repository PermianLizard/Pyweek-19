import comp
import util


class Entity(object):
    def __init__(self, owner=None):
        self.level = None
        self.owner = owner

    def update(self):
        pass


class Room(Entity):
    def __init__(self, area, owner=None):
        super(Room, self).__init__(owner)
        self.area = area
        self.level = None
        self.entry_points = None
        self.unique_entrance_count = 0

    def init(self):
        map = self.level.map

        room_padded_area = self.padded_area
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

        self.entry_points = list(room_entrances)

        unique_entry_points = len(self.entry_points)
        print unique_entry_points
        #for pos in self.entry_points:
        #    for other_pos in self.entry_points:
        #        if pos == other_pos:
        #            continue
        #        if

    @property
    def padded_area(self):
        return self.area.inflate(2, 2)


class Being(Entity):
    def __init__(self, speed, pos=(0, 0), owner=None):
        super(Being, self).__init__(owner)
        self.pos = pos
        self.owner = owner
        self.action = comp.ActionComp(speed)

    def init(self):
        pass

    def get_state(self):
        return self.action.get_being_state()

    def can_make_requests_of(self, other):
        return True

    def update(self):
        if self.action.delay <= 0:
            action = self.action.top_action()
            if action:
                action(self)
                if action.complete:
                    self.action.pop_action()
            self.action.delay = 100 // self.action.speed
        else:
            self.action.delay -= 1