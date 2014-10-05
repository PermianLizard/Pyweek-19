import pygame

from core import director
from core.scene import SceneLayer

import game

class GameLayer(SceneLayer):
    def draw(self, surf):
        game_instance = game.instance

        surf_size = surf.get_size()

        pygame.draw.rect(surf, (255, 255, 255), (100, 100, 32, 32))
