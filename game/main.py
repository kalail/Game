import config
import engine
import engine.adapters
import logging
from levels import TestLevel


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
    l = TestLevel()
    e = engine.Engine(l, c, adapter)
    # Run engine
    e.start()

if __name__ == '__main__':
    main()