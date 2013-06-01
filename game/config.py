
class Config(object):
    """Config

    Represents the current game configurations.

    """
    def __init__(self):
        self.title = 'Game'
        self.width = 640
        self.height = 360
        self.resolution = (self.width, self.height)
        self.fullscreen = False
        self.framerate = 60
        self.check_bounds = True
        self.debug = True

    def save(self):
        """Save
        
        Saves the configuration options to disk.

        """
        pass