
import pygame
import math
import helpers


class Movable(object):
    """Movable

    Any object that can move.

    Needs:

        position*

    """
    def __init__(self, position=None, **kwargs):
        if not position:
            raise Exception
        self.update_position(position)
        super(Movable, self).__init__(**kwargs)

    def _update_ext_position(self):
        """Update external position representation from internal floating point position."""
        pos = self._position
        self.position = (int(pos[0]), int(pos[1]))

    def update_position(self, pos):
        """Update internal and then external positions."""
        self._position = (float(pos[0]), float(pos[1]))
        self._update_ext_position()

    def move(self, delta=(0.0, 0.0)):
        pos_x = self._position[0] + float(delta[0])
        pos_y = self._position[1] + float(delta[1])
        self.update_position((pos_x, pos_y))


class Rotatable(object):
    """Rotatable

    Any object that can rotate.

    Needs:

        rotation*

    """
    def __init__(self, rotation=0.0, **kwargs):
        # direction = (180.0/math.pi) * (math.atan((direction[0]/direction[1])))
        self.rotation = float(rotation)
        self._update_rotation()
        super(Rotatable, self).__init__(**kwargs)

    def _update_rotation(self):
        # Update vertices
        rotation = math.radians(self.rotation)
        self.rotated_vertices = []
        for v in self.vertices:
            x = v[0] * math.cos(rotation) + v[1] * math.sin(rotation)
            y = v[1] * math.cos(rotation) - v[0] * math.sin(rotation)
            self.rotated_vertices.append((x, y))

    @property
    def orientation(self):
        rotation = math.radians(self.rotation)
        x = math.sin(rotation)
        y = math.cos(rotation)
        normalized = helpers.normalize((x, y))
        return normalized

    def set_rotation(self, rot=0.0):
        self.rotation = float(rot)
        self._update_rotation()

    def rotate(self, delta=0.0):
        self.rotation += delta
        self._update_rotation()

    def face(self, pos):
        direction = helpers.get_direction(self.position, pos)
        if 0 in direction:
            return
        rotation = (180.0/math.pi) * (math.atan((direction[0]/direction[1])))
        self.set_rotation(rotation)


class EntityLink(object):
    """Entity Link

    Link to entity manager.

    Needs:

        link*

    """
    def __init__(self, link=None, **kwargs):
        if not link:
            raise Exception
        self.link = link
        super(EntityLink, self).__init__(**kwargs)


class Renderable(object):
    """Renderable

    Allows object to be.

    """
    def __init__(self, **kwargs):
        pass


class SimpleRenderable(object):
    """Simple Renderable

    Allows object to be rendered using pygame polygon rendering.

    Needs:
    
        vertices
        color
    
    """
    def __init__(self, **kwargs):
        if not self.vertices:
            raise Exception
        if not self.color:
            raise Exception
        super(SimpleRenderable, self).__init__(**kwargs)

    def render(self):
        return (self.vertices, self.color)

# class Renderable(Sprite):
#     """Renderable

#     Component that manages rendering and loading of assets for objects

#     """
#     def __init__(self, image, orientation=None):
#         super(Renderable, self).__init__()
#         self.image = self._load_image(image)
#         if not len(position) == 2:
#             raise TypeError('Position not of length 2')
#         self.position = position
#         self.rect = self._create_rect()

#     def _create_rect(self):
#         rect = self.image.get_rect()
#         rect.center = self.position
#         return rect

#     def _load_image(self, img_file):
#         try:
#             image = pygame.image.load(img_file).convert_alpha()
#         except pygame.error as error:
#                 msg = 'Cannot load image: %s' % error
#                 logging.error(msg)
#                 raise IOError(msg)
#         return image

#     def scale(self, size):
#         self.image = pygame.transform.scale(self.image, (size, size))
#         self.rect = self._create_rect()
        

#     def move(self, x, y):
#         new_x = float(self.position[0]) + float(x)
#         new_y = float(self.position[1]) + float(y)
#         self.position = (int(new_x), int(new_y))
#         self.rect.center = self.position

#     def remove(self):
#         pass

#     def __str__(self):
#         return 'Game Object %s' % self.image

#     def __del__(self):
#         self.remove()


class Animatable(object):
    pass