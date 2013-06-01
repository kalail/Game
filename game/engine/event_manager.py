import PAL

class EventManager(object):
    """Event Manager

    Manages events for the engine.

    """

    def __init__(self):
        pass

    def get(self):
        return PAL.get_events()