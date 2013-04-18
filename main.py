import config
import engine

        
if __name__ == '__main__':
    config = config.Config()
    engine = engine.Engine(config)
    engine.start()
