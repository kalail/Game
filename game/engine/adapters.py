import pygame
import pygame.locals as pylocals
import logging

class PygameAdapter(object):
    """Pygame Adapter

    Allows the game engine to work on pygame.

    """

    def __init__(self):
        pygame.init()

    def create_screen(self, resolution, fullscreen, hardware=True, opengl=False, double_buffer=True):
        flags = 0
        if fullscreen:
            flags |= pylocals.FULLSCREEN
            if hardware:
                flags |= pylocals.HWSURFACE
                if opengl:
                    flags |= pylocals.OPENGL
                if double_buffer:
                    flags |= pylocals.DOUBLEBUF
        if not pygame.display.mode_ok(resolution, flags):
            logging.warning('Display mode not fully supported')
        return pygame.display.set_mode(resolution, flags)

    def create_sound(size):
        if size:
            screen = pygame.display.set_mode(size, pylocals.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(size)
        return screen