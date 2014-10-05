import pygame
from core import color
from consts import DISPLAY_SIZE, TILE_SIZE
import resources
import game


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
    map = level.map
    tile_surf = resources.image_cache.get_tile(resources.image__tileset1, (0, 0))

    x, y = tile

    if (map.get_tile(x, y).type == game.tile_type_wall):
        surf.blit(tile_surf, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))