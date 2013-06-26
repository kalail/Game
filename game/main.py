import json
import logging
import engine
from game import TestGame
# from numba import autojit

# @autojit
def main():
    # Setup simple logging
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        level=logging.INFO
    )
    # Get config
    with open('config.json') as config_file:
        config = json.load(config_file)
    # Start engine
    game_cls = TestGame
    eng = engine.Engine(config, game_cls)
    # Run engine
    eng.start()

if __name__ == '__main__':
    main()