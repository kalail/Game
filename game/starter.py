import sys
import os
import json
import engine
from game import TestGame

class Starter(object):
    """Starter

    Manages the startup of the game engine.

    """
    required_files = frozenset([
        'engine',
        'config.json',
        'main.py',
    ])

    @staticmethod
    def validate(files):
        files_not_found = Starter.required_files - files
        if files_not_found:
            raise RuntimeError('files {} not found'.format(list(files_not_found)))

    def __init__(self):
        cur_dir = os.getcwd()
        root_files = frozenset(os.listdir(cur_dir))
        # Check for required files
        # Get config options
        # Create engine
        Starter.validate(root_files)
        config = Config('config.json')
        self.engine = engine.Engine(config, TestGame)
        raise Exception()

    def start(self):
        self.engine.start()


class Config(dict):
    
    def __init__(self, path):
        with open(path) as config_file:
            config = json.load(config_file)
        super(Config, self).__init__(config)
        self['platform'] = sys.platform