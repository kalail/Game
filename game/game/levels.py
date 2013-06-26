import entities
from engine.object_manager import BuildOrder
from engine import colors


class TestLevel(object):
    """Test Level

    A game level with interfaces to run and describe the level.

    """
    

    size = (640.0, 360.0)

    theme = {
        'clear': colors.white,
        'black': colors.black,
        'white': colors.white,
        'red': colors.red,
        'blue': colors.blue,
    }

    starting_entities = [
        BuildOrder(entities.Test, position=(0, 0)),
        # BuildOrder(units.Bullet, position=(80, 120), target=(300, 300)),
    ]