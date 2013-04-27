import pygame
import theme
from .base import Thing, GameObject
import Queue
import helpers
import random
import logging


class Pulse(Thing):
    """Pulse

    Shot by a pulse rilfe

    """
    def __init__(self, direction, color=theme.black, *args, **kwargs):
        super(Pulse, self).__init__(*args, **kwargs)
        self.length = 8
        self.color = color
        self.speed = 1200.0
        self.direction = direction
        self._length_half = self.length / 2.0

    def update(self, delta, **kwargs):
        dist = self.speed * delta
        dist_x = self.direction[0] * dist
        dist_y = self.direction[1] * dist
        self.move(dist_x, dist_y)

    def draw(self, screen):
        line_start_x = self.position[0] - self.direction[0] * self.length
        line_start_y = self.position[1] - self.direction[1] * self.length
        line_end_x = self.position[0] + self.direction[0] * self.length
        line_end_y = self.position[1] + self.direction[1] * self.length
        pygame.draw.line(screen, self.color, (line_start_x, line_start_y), (line_end_x, line_end_y))

    def __str__(self):
        return 'Pulse'


class Bot(GameObject):
    """Bot

    Basic tier 1 unit.

    """
    def __init__(self, position):
        super(Bot, self).__init__('assets/circle.png', position)
        self.scale(20)
        pygame.transform.scale
        self.speed = 150.0
        self.fire_rate = 3.0
        self._fire_delay = 1.0 / self.fire_rate
        self._fire_timer = 0.0
        self._firing = False
        # _random_aim = lambda: -30.0 + random.random()*60.0
        # self.aim = None

    def _fire(self, position):
        diff_x = position[0] - self.position[0]
        diff_y = position[1] - self.position[1]
        aim = helpers.normalize((diff_x, diff_y))
        return Pulse(direction=aim, position=self.position)

    def fire(self, target):
        if self._fire_timer >= self._fire_delay:
            self._fire_timer = 0.0
            return self._fire(target.position)


    def update(self, delta, **kwargs):
        dist = self.speed * delta
        self.move(dist, 0)
        # targets = self.check_for_targets(kwargs['command_link'])
        if self._fire_timer < self._fire_delay:
            self._fire_timer += delta
        # if targets:
        #     target = random.choice(targets)
        #     shot = self.fire(target)
        #     if shot:
        #         return [shot]
        return []

    def __str__(self):
        return 'Bot'


class Home(GameObject):
    """Home

    Home base for a player that creates list of units periodically.

    """
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
        self._current_timer += delta
        
        num_units = int(self._current_timer / self.target_period)
        if num_units > 0:
            self._current_timer = 0.0
        return num_units

    def _queue_get_new(self, num_units):
        pending = []
        if num_units == 0:
            return []
        for i in range(num_units):
            try:
                unit_type = self.build_queue.get_nowait()
            except Queue.Empty:
                break
            pos = self._next_pos()
            unit = unit_type(position=pos)
            pending.append(unit)
        return pending

    def update(self, delta, **kwargs):
        num_units = self._process_queue(delta)
        new_units = self._queue_get_new(num_units)
        return new_units

    def draw(self, screen):
        if self.side == 'left':
            pygame.draw.rect(screen, self.color, (0, 0, 20, screen.get_height()) )
        elif self.side == 'right':
            pygame.draw.rect(screen, self.color, (screen.get_width() - 20, 0, 20, screen.get_height()))

    def __str__(self):
        return 'Home'