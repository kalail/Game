import pygame
import theme
from base import Thing

class Bot(Thing):

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.radius = 5
        self.color = theme.red
        self.speed = 0.1

    def update(self, delta):
        dist = self.speed * delta
        self.move(dist, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def __str__(self):
        return 'Bot'