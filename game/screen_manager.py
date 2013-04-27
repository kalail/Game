import pygame
import pygame.locals as pylocals

class ScreenManager(object):

    def __init__(self, resolution, fullscreen=False, hardware=False):
        self.screen = self._create_screen(resolution, fullscreen, hardware)

    def _create_screen(self, resolution, fullscreen, hardware):
        flags = 0
        if fullscreen:
            flags = pylocals.FULLSCREEN
        return pygame.display.set_mode(resolution, flags)