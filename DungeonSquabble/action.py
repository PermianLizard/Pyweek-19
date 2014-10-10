import operator
import util

class Action(object):
    def __init__(self, name):
        self.name = name
        self.complete = False

    def __call__(self, being):
        pass


class MoveAction(Action):
    name = 'Move'

    def __init__(self, path):
        super(MoveAction, self).__init__(MoveAction.name)
        self.path = path
        self.blocked_count = 0


    def __call__(self, being):
        path = self.path
        if path:
            next_pos = path[0]
            if not being.pos == next_pos:
                level = being.level

                beings_blocking_me = level.get_beings_at(*next_pos)
                if beings_blocking_me:
                    self.blocked_count += 1
                    for blocking_being in beings_blocking_me:
                        if blocking_being.get_state() != MoveAction.name:
                            blocking_being.action.push_action(MakeWayAction(being))
                else:
                    being.pos = next_pos
                    self.blocked_count = 0
                    path.pop(0)
            else:
                path.pop(0)

            if not path:
                self.complete = True

            if self.blocked_count >= 20:  # give up
                self.complete = True


class MakeWayAction(Action):
    name = 'Make Way'

    def __init__(self, for_being):
        super(MakeWayAction, self).__init__(MakeWayAction.name)
        self.for_being = for_being
        self.for_pos = for_being.pos
        self.blocked_count = 0

    def __call__(self, being):
        for_pos = self.for_pos
        if util.tiles_adjacent(being.pos, for_pos):
            possible_move_to = util.get_adjacent_tiles(*being.pos)

            if possible_move_to:
                possible_move_to = being.level.filter_passable(possible_move_to)
                if possible_move_to:
                    d = {pos: util.distance(for_pos, pos) for pos in possible_move_to}
                    s = sorted(d.keys(), key=operator.itemgetter(1))

                    next_pos = s[0]

                    being.pos = next_pos

        self.complete = True
