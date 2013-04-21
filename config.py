

class Config(object):
    """Config

    Represents the current game configurations.

    """
    def __init__(self):
        self.title = 'Hello World!'
        self.width = 640
        self.height = 360
        self.size = (self.width, self.height)
        self.framerate = 60
        self.check_bounds = True
        