import pygame

from . import director


class Quit(Exception):
    pass


def run(scene, screen_size=(800, 600), display_size=(800, 600), fps=30, on_init=None):
    pygame.init()

    display = pygame.display.set_mode(screen_size)
    screen = pygame.Surface(display_size).convert()

    clock = pygame.time.Clock()
    ticks = 0

    director.push(scene)

    if on_init:
        on_init()

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

            real_fps = clock.get_fps()
            keys = pygame.key.get_pressed()

            top.update(fps=real_fps, keys=keys)
            top.draw(screen, fps=real_fps, keys=keys)

        except Quit:
            break

        pygame.transform.scale(screen, screen_size, display)
        pygame.display.update()

        clock.tick(fps)

    while director.top():
        director.pop()

    pygame.mixer.music.stop()
    pygame.quit()
