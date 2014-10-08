import pygame
from core import color
from consts import DISPLAY_SIZE, TILE_SIZE, HALF_TILE_SIZE
import resources
import game


def create_level_surf(level):
    map = level.map
    surf_size = map.size[0] * TILE_SIZE, map.size[1] * TILE_SIZE
    surf = pygame.Surface(surf_size)
    surf.convert()

    return surf


def render_level_beings(surf, level, camera):
    for being in level.beings:
        render_being(surf, being, camera)


def render_being(surf, being, camera):
    pos = being.pos
    cx, cy = camera.view.topleft

    pygame.draw.circle(surf, color.GREEN,
                       (pos[0] * TILE_SIZE + HALF_TILE_SIZE - cx, pos[1] * TILE_SIZE + HALF_TILE_SIZE - cy),
                       HALF_TILE_SIZE - 1)


def render_level_rooms(surf, level, camera):
    for room in level.rooms:
        render_room(surf, room, camera)


def render_room(surf, room, camera):
    area = room.area
    cx, cy = camera.view.topleft

    pygame.draw.rect(surf, color.RED, (area.left * TILE_SIZE - cx,
                                       area.top * TILE_SIZE - cy,
                                       area.width * TILE_SIZE,
                                       area.height * TILE_SIZE))

    for x, y in room.entry_points:
        pygame.draw.rect(surf, color.BLUE, (x * TILE_SIZE - cx, y * TILE_SIZE - cy, TILE_SIZE, TILE_SIZE))


def render_level_map(surf, level, camera=None):
    map = level.map
    for y in xrange(map.size[1]):
        for x in xrange(map.size[0]):
            render_map_tile(surf, level, (x, y))


def render_map_tile(surf, level, tile):
    map = level.map

    x, y = tile

    if (map.get_tile(x, y).type == game.tile_type_wall):
        pygame.draw.rect(surf, color.GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
