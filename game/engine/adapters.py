import pygame
import pygame.locals as pylocals
import logging

class PygameAdapter(object):
    """Pygame Adapter

    Allows the game engine to work on pygame.

    """

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(0)

    def create_surface(self, resolution, fullscreen, hardware=True, opengl=False, double_buffer=True):
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

    def load_sound(self, asset):
        return pygame.mixer.Sound(asset)

    def get_clock(self):
        return pygame.time.Clock()

    def clear(self, screen, color):
        screen.fill(color)

    def flip(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()
