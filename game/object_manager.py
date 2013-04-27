import pygame
from pygame.sprite import Group


class ObjectManager(Group):
    """Object Manager

    Handles units for engine.
    
    """
    def __init__(self, objects):
        super(ObjectManager, self).__init__()
        for o in objects:
            self.add(o)

    def update(self, delta):
        new_objects = []
        for o in self.sprites():
            possible_objects = o.update(delta)
            if possible_objects:
                new_objects.append(possible_objects)
        flat = []
        [flat.extend(objects) for objects in new_objects]
        return flat