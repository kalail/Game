import sys
import pygame
import pygame.locals as pylocals
import theme


def handle_pointer(event, pointer):
    if event.type == 4:
        if pointer.down:
            print 'Pointer Drag'
        else:
            print 'Pointer Move'
    elif event.type == 5:
        if not pointer.down:
            pointer.down = True
            print 'Pointer Down'
    elif event.type == 6:
        if pointer.down:
            pointer.down = False
            print 'Pointer Up'


class Pointer(object):
    
    def __init__(self):
        self.down = False

class Engine(object):

    def __init__(self, config):
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode(self.config.size)
        pygame.display.set_caption(self.config.title)
        self.timer = pygame.time.Clock()
        self.pointer = Pointer()
        self.objects = [Thing(40, 40), Thing(60, 20), Thing(60, 40), Thing(20, 50), Thing(90, 70), Thing(30, 70)]

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
                handle_pointer(event, self.pointer)

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


class Thing(object):

    def __init__(self, x, y):
        self.color = theme.red
        self.radius = 5
        self.x = x
        self.y = y
        self.position = (self.x, self.y)

    def move(self, x, y):
        self.x += x
        self.y += y
        self.position = (self.x, self.y)

    def update(self, delta):
        dist = int(0.1*delta)
        self.move(dist, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def __str__(self):
        return 'Thing'




class Config(object):

    def __init__(self):
        self.title = 'Hello World!'
        self.width = 640
        self.height = 360
        self.size = (self.width, self.height)
        self.framerate = 30
        self.check_bounds = True
        
if __name__ == '__main__':
    config = Config()
    engine = Engine(config)
    engine.start()
