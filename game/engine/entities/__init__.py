import pygame
import logging
from pygame.sprite import Sprite
import types
import helpers

class GameObject(Sprite):
    """Game Object

    Base class for any object in the game.
    
    """
    image = None

    def __init__(self, image, position, orientation=None):
        super(GameObject, self).__init__()
        self.image = self._load_image(image)
        if not len(position) == 2:
            raise TypeError('Position not of length 2')
        self.position = position
        self.rect = self._create_rect()

    def _create_rect(self):
        rect = self.image.get_rect()
        rect.center = self.position
        return rect

    def _load_image(self, img_file):
        try:
            image = pygame.image.load(img_file).convert_alpha()
        except pygame.error as error:
                msg = 'Cannot load image: %s' % error
                logging.error(msg)
                raise IOError(msg)
        return image

    def scale(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self._create_rect()
        

    def move(self, x, y):
        new_x = float(self.position[0]) + float(x)
        new_y = float(self.position[1]) + float(y)
        self.position = (int(new_x), int(new_y))
        self.rect.center = self.position

    def remove(self):
        pass

    def __str__(self):
        return 'Game Object %s' % self.image

    def __del__(self):
        self.remove()


class Entity(object):
    """Entity

    Base class for any object in the game engine.
    
    """

    def __init__(self, **kwargs):
        if not self.name:
            raise Exception
        super(Entity, self).__init__(**kwargs)

    def start(self):
        pass

    def end(self):
        pass

    def update(self, delta):
        super(Entity, self).update(delta)

    def __str__(self):
        return 'Entity %s' % self.name

    def run_if_has(self, func, *args, **kwargs):
        try:
            attr = getattr(self, func)
        except AttributeError:
            return
        else:
            return attr(*args, **kwargs)

    def __del__(self):
        self.end()