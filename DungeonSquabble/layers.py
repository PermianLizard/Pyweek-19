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
