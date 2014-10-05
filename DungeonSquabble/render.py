import pygame
from core import color
from consts import DISPLAY_SIZE, TILE_SIZE


def create_level_surf(level):
    map = level.map
    surf_size = map.size[0] * TILE_SIZE, map.size[1] * TILE_SIZE
    surf = pygame.Surface(surf_size)
    surf.convert()

    return surf


def render_level_map(surf, level):
    map = level.map
    for y in xrange(map.size[1]):
        for x in xrange(map.size[0]):
            render_map_tile(surf, level, (x, y))


def render_map_tile(surf, level, tile):
    x, y = tile
    pygame.draw.rect(surf, color.RED, (x * TILE_SIZE,
                                       y * TILE_SIZE,
                                       TILE_SIZE - 1,
                                       TILE_SIZE - 1))
