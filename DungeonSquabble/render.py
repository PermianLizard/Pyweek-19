import pygame
from core import color
from DungeonSquabble.consts import DISPLAY_SIZE, TILE_SIZE, HALF_TILE_SIZE
from DungeonSquabble import resources
from DungeonSquabble import game
from DungeonSquabble import gameobj


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

    rect = (pos[0] * TILE_SIZE + HALF_TILE_SIZE - cx, pos[1] * TILE_SIZE + HALF_TILE_SIZE - cy)

    pygame.draw.circle(surf, being.owner.light_color,
                       rect,
                       HALF_TILE_SIZE - 1)


def render_level_rooms(surf, level, camera):
    for room in level.rooms:
        render_room(surf, room, camera)


def render_room(surf, room, camera):
    area = room.area
    cx, cy = camera.view.topleft

    rect = (area.left * TILE_SIZE,
            area.top * TILE_SIZE,
            area.width * TILE_SIZE,
            area.height * TILE_SIZE)

    if not camera.view.colliderect(rect):
        return

    pygame.draw.rect(surf, room.owner.dark_color, (rect[0] - cx, rect[1] - cy, rect[2], rect[3]))

    #for x, y in room.entry_points:
    #    rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    #    pygame.draw.rect(surf, color.BLUE, (rect[0] - cx, rect[1] - cy, rect[2], rect[3]))


def render_level_map(surf, level, camera=None):
    map = level.map
    for y in range(map.size[1]):
        for x in range(map.size[0]):
            render_map_tile(surf, level, (x, y))


def render_map_tile(surf, level, tile):
    map = level.map

    x, y = tile

    if map.get_tile(x, y).type == gameobj.tile_type_wall:
        pygame.draw.rect(surf, color.GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
