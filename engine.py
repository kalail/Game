import pygame
import pointer
import units
import pygame.locals as pylocals
import theme
import sys
import base



class Engine(object):

    def __init__(self, config):
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode(self.config.size)
        pygame.display.set_caption(self.config.title)
        self.timer = pygame.time.Clock()
        self.pointer = pointer.Pointer()
        self.objects = [units.Home(side='left', color=theme.red, build_queue=[units.Bot, units.Bot, units.Bot, units.Bot])]

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
            if isinstance(o, base.Thing):
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
        new_objects = []
        for o in self.objects:
            possible_objects = o.update(delta)
            if possible_objects:
                print 'New object added'
                new_objects.append(possible_objects)
        [self.objects.extend(objects) for objects in new_objects]

    def draw(self):
        self.screen.fill((240,240,250))
        pygame.draw.rect(self.screen, theme.blue,  (10, 10, 10, 10))
        for o in self.objects:
            o.draw(self.screen)
        pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()