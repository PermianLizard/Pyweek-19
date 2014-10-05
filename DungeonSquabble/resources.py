import pygame
import os

from core import resource
import data


def load_font(filename, size):
    return pygame.font.Font(data.filepath(os.path.join('fonts', filename)), size)


def get_font(font):
    return font_cache.get(font[0], font[1])


def init():
    global font_cache
    font_cache = resource.FontResourceCache(data.filepath('fonts'))
    for name, size in fonts:
        font_cache.register(name, load_font, size)


font_cache = None
font__press_start_normal = 'PressStart2P.ttf', 12
fonts = font__press_start_normal,

