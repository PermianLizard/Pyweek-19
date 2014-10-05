import pygame
import os

from core import resource
from consts import TILE_SIZE
import data

def load_image(filename):
    img = pygame.image.load(data.filepath(os.path.join('images', filename)))
    #img.set_colorkey(TRANSPARENCY_COLOR_KEY)
    return img

def load_font(filename, size):
    return pygame.font.Font(data.filepath(os.path.join('fonts', filename)), size)


def get_font(font):
    return font_cache.get(font[0], font[1])


def init():
    global image_cache
    image_cache = resource.TiledImageResourceCache(data.filepath('images'), tile_size=(TILE_SIZE, TILE_SIZE))
    image_cache.register(image__tileset1, load_image)

    global font_cache
    font_cache = resource.FontResourceCache(data.filepath('fonts'))
    for name, size in fonts:
        font_cache.register(name, load_font, size)


image_cache = None
image__tileset1 = 'tileset1.png'

font_cache = None
font__press_start_normal = 'PressStart2P.ttf', 8
fonts = font__press_start_normal,

