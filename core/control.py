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
                elif event.type == pygame.KEYDOWN:
                    top.on_key_down(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    top.on_key_up(event.key, event.mod)
                elif event.type == pygame.MOUSEMOTION:
                    top.on_mouse_motion(event.pos, event.rel, event.buttons)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    top.on_mouse_button_down(event.pos, event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    top.on_mouse_button_up(event.pos, event.button)

            top.update(0)
            top.draw(screen)

        except Quit:
            break

        pygame.transform.scale(screen, display_size, display)
        pygame.display.update()

        clock.tick(fps)

    pygame.mixer.music.stop()
    pygame.quit()
