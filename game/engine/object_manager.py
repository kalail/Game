from pygame.sprite import Group
import PAL
import entities.components as components

class ObjectManager(Group):
    """Object Manager

    Handles units for engine.
    
    """
    def __init__(self):
        super(ObjectManager, self).__init__()

    def add_multiple(self, objects):
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



class BuildOrder(object):
    """Build Order

    Holds information requierd by the Entity Manager to build an Entity.

    """

    def __init__(self, entity_class, **kwargs):
        self.entity_class = entity_class
        self.params = kwargs


class EntityManager(object):
    """Entity Manager

    Handles all entity interaction in and with the game engine.
    
    Uses a group based system to manage entity groups.

    """
    groups = [
        'draw',
        'logical',
        '',
    ]
    def __init__(self, groups=None):
        if not groups:
            self.entities = []
        else:
            self.groups = {}
            for g in groups:
                self.groups[g] = []


    def add(self, entity):
        self.entities.append(entity)

    def add_multiple(self, entities=[]):
        for e in entities:
            self.add(e)

    def build(self, order):
        params = order.params
        if issubclass(order.entity_class, components.EntityLink):
            params['link'] = self
        entity = order.entity_class(**params)
        self.add(entity)

    def build_multiple(self, orders=[]):
        for o in orders:
            self.build(o)

    def remove(self, entity):
        index = self.entities.index(entity)
        e = self.entities.pop(index)
        e.end()
            
    def update(self, delta):
        # Update all entities
        new_orders = []
        for e in self.entities:
            possible_orders = e.update(delta)
            # Check for returned orders
            if possible_orders:
                new_orders.append(possible_orders)
        # Flatten entity list
        flat = []
        [flat.extend(order) for order in new_orders]
        # Add entities into active_list
        self.build_multiple(flat)

    def get_target(self):
        return PAL.get_pointer_position()