import pygame
from core import director
from core.scene import Scene
import game
import layers


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__(
            layers=[layers.DebugLayer(), layers.GameLayer()])

    def enter(self, **kwargs):
        game.new()
        super(GameScene, self).enter(**kwargs)

    def on_key_down(self, key, mod):
        if key == pygame.K_ESCAPE:
            director.pop()

    def update(self, **kwargs):
        super(GameScene, self).update(**kwargs)
        instance = game.instance
        instance.update(**kwargs)

if __name__ == '__main__':
    from core import control
    control.run(GameScene())
