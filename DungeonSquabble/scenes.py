import pygame

from core import director
from core.scene import Scene

import game


class GameScene(Scene):
    def __init__(self):
        pass

    def enter(self, **kwargs):
        super(GameScene, self).enter(**kwargs)
        game.new()

    def on_key_down(self, key, mod):
        if key == pygame.K_ESCAPE:
            director.pop()


if __name__ == '__main__':
    from core import control
    control.run(GameScene())
