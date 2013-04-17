import sys
import pygame
import pygame.locals as pylocals
import theme
from config import Config
import units

import pointer

class Engine(object):

    def __init__(self, config):
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode(self.config.size)
        pygame.display.set_caption(self.config.title)
        self.timer = pygame.time.Clock()
        self.pointer = pointer.Pointer()
        self.objects = [units.Bot((40, 40)), units.Bot((60, 20)), units.Bot((60, 40))]

    def start(self):
        self.run()

    def run(self):
        delta = 0
        while True:
            self.handle_events()
            self.update(delta)
            if self.config.check_bounds:
                self.check_bounds()
            self.draw()
            delta = self.timer.tick(self.config.framerate)

    def check_bounds(self):
        for o in self.objects:
            in_screen = ((0 < o.position[0] < self.config.width), (0 < o.position[1] < self.config.height))
            if False in in_screen:
                print 'Removing out of bound object {0}'.format(o)
                self.objects.remove(o)

    def handle_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pylocals.QUIT:
                self.quit()
            else:
                pointer.handle_pointer(event, self.pointer)

    def update(self, delta):
        for o in self.objects:
            o.update(delta)

    def draw(self):
        self.screen.fill((240,240,250))
        pygame.draw.rect(self.screen, theme.blue,  (10, 10, 10, 10))
        for o in self.objects:
            o.draw(self.screen)
        pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()


        
if __name__ == '__main__':
    config = Config()
    engine = Engine(config)
    engine.start()
