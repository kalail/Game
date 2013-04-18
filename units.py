import pygame
import theme
from base import Thing
import Queue
import helpers
import random

class Bot(Thing):

    def __init__(self, color=theme.red, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.radius = 5
        self.color = color
        self.speed = 0.1

    def update(self, delta):
        dist = self.speed * delta
        self.move(dist, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def __str__(self):
        return 'Bot'


class Home(object):

    def __init__(self, side='left', color=theme.red, rate=1, build_queue=[], *args, **kwargs):
        # super(Home, self).__init__(*args, **kwargs)
        self.side = side
        self.color = color
        self.rate = float(rate)
        self.target_period = 1.0 / self.rate
        self.build_queue = self._build_queue(build_queue)
        self._current_timer = 0.0

    def _build_queue(self, unit_types):
        num_units = len(unit_types)
        queue = Queue.Queue(num_units)
        for unit_type in unit_types:
            queue.put(unit_type)
        return queue

    def _next_pos(self):
        x = 10
        y = int(random.random() * 360)
        return (x, y)

    def _process_queue(self, delta):
        converted_delta = float(delta) / 1000.0
        self._current_timer += converted_delta
        
        num_units = int(self._current_timer / self.target_period)
        if num_units > 0:
            self._current_timer = 0.0
        return num_units

    def _queue_get_new(self, num_units):
        pending = []
        for i in range(num_units):
            try:
                unit_type = self.build_queue.get_nowait()
            except Queue.Empty:
                break
            pos = self._next_pos()
            unit = unit_type(position=pos)
            pending.append(unit)
        return pending

    def update(self, delta):
        num_units = self._process_queue(delta)
        new_units = self._queue_get_new(num_units)
        if not isinstance(new_units, list):
            new_units = [new_units]
        return new_units

    def draw(self, screen):
        if self.side == 'left':
            pygame.draw.rect(screen, self.color, (0, 0, 20, screen.get_height()) )
        elif self.side == 'right':
            pygame.draw.rect(screen, self.color, (screen.get_width() - 20, 0, 20, screen.get_height()))

    def __str__(self):
        return 'Bot'