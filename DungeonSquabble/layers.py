import pygame
import operator
from core import color
from core.scene import SceneLayer
from core.camera import Camera
import game
import resources
import text

from consts import DISPLAY_SIZE, TILE_SIZE, HALF_TILE_SIZE, DEBUG
from resources import font__press_start_normal


class GameLayer(SceneLayer):
    def draw(self, surf, **kwargs):
        game_instance = game.instance

        level = game_instance.state.get_current_level()
        map = level.map

        camera = self.camera

        for y in xrange(map.size[1]):
            for x in xrange(map.size[0]):
                pygame.draw.rect(surf, color.RED, (x * TILE_SIZE - camera.pos[0],
                                                   y * TILE_SIZE - camera.pos[1],
                                                   TILE_SIZE - 1,
                                                   TILE_SIZE - 1))

    def enter(self, **kwargs):
        game_instance = game.instance
        level = game_instance.state.get_current_level()
        map = level.map

        camera_limits = pygame.Rect(0, 0, map.size[0] * TILE_SIZE, map.size[1] * TILE_SIZE)
        camera_limits.width = max(camera_limits.width, DISPLAY_SIZE[0])
        camera_limits.height = max(camera_limits.height, DISPLAY_SIZE[1])
        camera_limits.inflate_ip(DISPLAY_SIZE[0] // 2, DISPLAY_SIZE[1] // 2)

        self.camera = Camera(DISPLAY_SIZE, pos=(0, 0), pan_speed=HALF_TILE_SIZE, limits=camera_limits)

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
