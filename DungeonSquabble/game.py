from DungeonSquabble import gameobj


class GameInstance(object):
    def __init__(self, state):
        self.state = state

        self.observers = []

    def notify(self, name, *args, **kwargs):
        for o in self.observers:
            o.notify(name, *args, **kwargs)

    def update(self, **kwargs):
        self.state.get_current_level().update()


class GameInstanceState(object):
    def __init__(self, levels):
        self.current_level = 0
        self.levels = levels[:]

    def get_current_level(self):
        return self.levels[self.current_level]


instance = None


level_configs = (
    ((55, 55), 12345),
)

def new():
    levels = []
    for conf in level_configs:
        print(conf[0], conf[1])
        levels.append(gameobj.gen_level(conf[0], conf[1]))

    #levels = [gameobj.gen_level((40, 40))]

    state = GameInstanceState(levels)

    global instance
    instance = GameInstance(state)


