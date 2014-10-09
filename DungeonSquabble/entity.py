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
    def __init__(self, pos=(0, 0), owner=None):
        super(Being, self).__init__(owner)
        self.pos = pos
        self.owner = owner
        self.action_stack = []

    def top_action(self):
        action_stack = self.action_stack
        if action_stack:
            return action_stack[-1]
        return None

    def push_action(self, action):
        self.action_stack.append(action)

    def swap_action(self, action):
        action_stack = self.action_stack
        if action_stack:
            action_stack.pop()
        action_stack.append(action)

    def pop_action(self):
        action_stack = self.action_stack
        if action_stack:
            action_stack.pop()

    def update(self):
        action = self.top_action()
        if action:
            action(self)

            if action.complete:
                self.pop_action()
