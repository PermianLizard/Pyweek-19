import comp


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

    @property
    def padded_area(self):
        return self.area.inflate(2, 2)


class Being(Entity):
    def __init__(self, speed, pos=(0, 0), owner=None):
        super(Being, self).__init__(owner)
        self.pos = pos
        self.owner = owner
        self.action = comp.ActionComp(speed)

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