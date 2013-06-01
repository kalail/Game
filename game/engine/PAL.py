import pygame
import pygame.locals as pylocals
import logging

platforms = [
    'windows',
    'osx',
    'linux',
]

backends = [
    'pygame'
]

def init():
    pygame.init()
    pygame.mouse.set_visible(0)

def create_surface(resolution, fullscreen, hardware=False, opengl=True, double_buffer=True):
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

def get_pointer_position():
    return pygame.mouse.get_pos()

def load_image(asset):
    try:
        image = pygame.image.load(asset).convert_alpha()
    except pygame.error as error:
            logging.error('Cannot load image: %s' % error)
            # raise IOError()
    else:
        return image

def load_sound(asset):
    return pygame.mixer.Sound(asset)

def get_clock():
    return pygame.time.Clock()

def get_events():
    return pygame.event.get()
    
def clear_screen(screen, color):
    screen.fill(color)

def flip():
    pygame.display.flip()

def quit():
    pygame.quit()

