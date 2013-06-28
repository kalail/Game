import json
import logging
import engine
from game import TestGame
from starter import Starter
# from numba import autojit

# @autojit
def main():
    engine_starter = Starter()
    engine_starter.start()
    # Setup simple logging
    # logging.basicConfig(
    #     format='%(levelname)s:%(message)s',
    #     level=logging.INFO
    # )
    # Get config
    # Start engine

if __name__ == '__main__':
    main()