import pygame
from core import color
from core.scene import SceneLayer
import game
import resources
import text

from consts import DEBUG
from resources import font__press_start_normal


class GameLayer(SceneLayer):
    def draw(self, surf, **kwargs):
        game_instance = game.instance

        level = game_instance.state.get_current_level()
        map = level.map

        for y in xrange(map.size[1]):
            for x in xrange(map.size[0]):
                pygame.draw.rect(surf, color.RED, (x * 20, y * 20, 19, 19))

    def on_mouse_button_down(self, pos, button):
        print 'click'
        return False


class DebugLayer(SceneLayer):
    def draw(self, surf, **kwargs):
        if DEBUG:
            fps = kwargs['fps']
            surf_size = surf.get_size()
            text.draw(surf, 'FPS: %s' % fps,
                      font__press_start_normal,
                      (10, surf_size[1] - 5),
                      color.GRAY,
                      halign='left', valign='bottom')
