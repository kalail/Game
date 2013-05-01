import config
import engine
import engine.adapters
import logging

import cProfile


def main():
    # Setup simple logging
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        level=logging.INFO
    )
    # Get config
    c = config.Config()
    # Choose adapter
    adapter = engine.adapters.PygameAdapter
    # Start engine
    e = engine.Engine(c, adapter)
    # Run engine
    e.start()

if __name__ == '__main__':
    cProfile.run('main()')
