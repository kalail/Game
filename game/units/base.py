import pygame
import logging
from pygame.sprite import Sprite


class Thing(object):
    """Thing

    Base class for any unit with a position.
    
    """
    def __init__(self, position):
        self.position = position

    def move(self, x, y):
        new_x = float(self.position[0]) + float(x)
        new_y = float(self.position[1]) + float(y)
        self.position = (int(new_x), int(new_y))

    def __str__(self):
        return 'Thing'


class GameObject(Sprite):
    """Game Object

    Base class for any object with an image, a position and an orientation.

    Built on Pygame Sprites
    
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
            image = pygame.image.load(img_file)
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