import pygame
from core import color
from DungeonSquabble import resources

halign_left = 'left'
halign_center = 'center'
halign_right = 'right'

valign_top = 'top'
valign_center = 'center'
valign_bottom = 'bottom'

def draw(surf, text, font, pos, color=color.WHITE, halign='left', valign='bottom'):
    if not isinstance(font, pygame.font.Font):
        font = resources.get_font(font)

    text_surf = font.render(text, False, color)
    text_rect = text_surf.get_rect()

    text_rect.left = pos[0]
    if halign == halign_center:
        text_rect.centerx = pos[0]
    elif halign == halign_right:
        text_rect.right = pos[0]

    text_rect.top = pos[1]
    if valign == valign_center:
        text_rect.centery = pos[1]
    elif valign == valign_bottom:
        text_rect.bottom = pos[1]

    surf.blit(text_surf, text_rect)