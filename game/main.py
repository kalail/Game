import config
import engine
import engine.adapters
import logging


if __name__ == '__main__':
    # Setup simple logging
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        level=logging.INFO
    )
    # Get config
    config = config.Config()
    # Choose adapter
    adapter = engine.adapters.PygameAdapter
    # Start engine
    engine = engine.Engine(config, adapter)
    # Run engine
    engine.start()
