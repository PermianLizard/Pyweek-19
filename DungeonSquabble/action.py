class Action(object):
    def __init__(self, name):
        self.name = name
        self.complete = False

    def __call__(self, being):
        pass


class MoveAction(Action):
    def __init__(self, path):
        super(MoveAction, self).__init__('Move')
        self.path = path

    def __call__(self, being):
        path = self.path
        if path:
            next_pos = path.pop(0)
            being.pos = next_pos

            if not path:
                self.complete = True
