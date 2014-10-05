import pygame


class Camera(object):
    def __init__(self, size, pan_speed, pos=(0, 0), limits=None):
        self.view = pygame.Rect(tuple(pos + size))
        self.pan_speed = pan_speed
        self.limits = limits

    def pan(self, dir):
        horiz = self.pan_speed * dir[0]
        vert = self.pan_speed * dir[1]

        self.view.move_ip(horiz, vert)
        if self.limits:
            self.view.clamp_ip(self.limits)

    @property
    def pos(self):
        return self.view.topleft

    @property
    def size(self):
        return self.view.size