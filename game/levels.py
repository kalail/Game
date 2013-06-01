import units
from engine.object_manager import BuildOrder
class TestLevel(object):
    """Level

    A game level with interfaces to run and describe the level.

    """
    assets = [
        'assets/ThisUsedToBeACity.ogg',
        'assets/beep.ogg',
    ]

    def start(self):
        starting_units = [
        #     units.Bot((0, 0)),
        #     units.Bot((10, 50)),
        #     units.Bot((50, 80))
        ]
        return starting_units

    def starting_order(self):
        starting_units = [
            # BuildOrder(units.Test, position=(80, 120)),
            # BuildOrder(units.Bullet, position=(80, 120), target=(300, 300)),

        ]
        return starting_units