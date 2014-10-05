from core.scene import Scene


class GameScene(Scene):
    pass

if __name__ == '__main__':
    from core import control

    control.run(GameScene())