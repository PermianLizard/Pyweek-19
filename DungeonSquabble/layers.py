import pygame

from core import director
from core.scene import SceneLayer

import game
import resources
from consts import DEBUG

class GameLayer(SceneLayer):
    def draw(self, surf, **kwargs):
        game_instance = game.instance

        if DEBUG:
            pass

        fps = kwargs['fps']

        font = resources.get_font(resources.font__press_start_normal)
        fps_surf = font.render('FPS: %s' % fps, False, (255, 255, 255))
        fps_rect = fps_surf.get_rect()
        surf.blit(fps_surf, (10, 10))


        #font = resources.font_cache.get()

        #surf_size = surf.get_size()
        #pygame.draw.rect(surf, (255, 255, 255), (100, 100, 32, 32))
