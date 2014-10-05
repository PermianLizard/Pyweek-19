import pygame

from . import director


class Quit(Exception):
    pass


def run(scene, display_size=(800, 600), display_resolution=(800, 600), fps=30):
    pygame.init()

    display = pygame.display.set_mode(display_size)
    screen = pygame.Surface(display_resolution).convert()

    clock = pygame.time.Clock()

    director.push(scene)

    while True:
        top = director.top()
        if top is None:
            break

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise Quit()

            top.update(0)
            top.draw(screen)

        except Quit:
            break

        pygame.transform.scale(screen, display_size, display)
        pygame.display.update()

        clock.tick(fps)

    pygame.mixer.music.stop()
    pygame.quit()
