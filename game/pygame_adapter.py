import pygame
import pygame.locals as pylocals

class PygameAdapter(object):
    """Pygame Adapter

    Allows the game engine to work on pygame.

    """

    def __init__(self):
        pygame.init()

    def _create_screen(size, fullscreen):
        if fullscreen:
            screen = pygame.display.set_mode(size, pylocals.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(size)
        return screen