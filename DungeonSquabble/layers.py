import pygame
import operator
from core import color
from core.scene import SceneLayer
from core.camera import Camera
import game
import resources
import text
import render

from consts import DISPLAY_SIZE, TILE_SIZE, HALF_TILE_SIZE, DEBUG
from resources import font__press_start_normal


class GameLayer(SceneLayer):
    def __init__(self):
        super(GameLayer, self).__init__()
        self.camera = None
        self.map_surf = None

    def enter(self, **kwargs):
        game_instance = game.instance
        level = game_instance.state.get_current_level()
        map = level.map

        camera_limits = pygame.Rect(0, 0, map.size[0] * TILE_SIZE, map.size[1] * TILE_SIZE)
        camera_limits.width = max(camera_limits.width, DISPLAY_SIZE[0])
        camera_limits.height = max(camera_limits.height, DISPLAY_SIZE[1])
        camera_limits.inflate_ip(DISPLAY_SIZE[0] // 2, DISPLAY_SIZE[1] // 2)

        self.camera = Camera(DISPLAY_SIZE, pos=(0, 0), pan_speed=HALF_TILE_SIZE, limits=camera_limits)

        map_surf = render.create_level_surf(level)
        render.render_level_map(map_surf, level)
        self.map_surf = map_surf

    def update(self, **kwargs):
        keys = kwargs['keys']

        scroll_dir = [0, 0]
        if keys[pygame.K_LEFT]:
            scroll_dir[0] = -1
        if keys[pygame.K_RIGHT]:
            scroll_dir[0] = 1
        if keys[pygame.K_UP]:
            scroll_dir[1] = -1
        if keys[pygame.K_DOWN]:
            scroll_dir[1] = 1

        self.camera.pan(scroll_dir)

    def draw(self, surf, **kwargs):
        game_instance = game.instance

        level = game_instance.state.get_current_level()
        map = level.map

        camera = self.camera

        surf.blit(self.map_surf, (0, 0, camera.view.width, camera.view.height), camera.view)

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
                      color.WHITE,
                      halign='left', valign='bottom')
