import math
from consts import TILE_SIZE, RES_SCALE

def distance(l1, l2):
    return math.sqrt(math.pow(l2[0] - l1[0], 2) + math.pow(l2[1] - l1[1], 2))

def pixel_to_tile(pos, offset=None):
    if offset is not None:
        pos = int(pos[0] * RES_SCALE) + offset[0], int(pos[1] * RES_SCALE) + offset[1]
    return pos[0] // TILE_SIZE, pos[1] // TILE_SIZE