import config
import engine
import logging

if __name__ == '__main__':
    # Setup simple logging
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        level=logging.WARNING
    )
    # Get config
    config = config.Config()
    # Start engine
    engine = engine.Engine(config)
    # Run engine
    engine.start()
