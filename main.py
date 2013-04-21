import config
import engine
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    config = config.Config()
    engine = engine.Engine(config)
    engine.start()
