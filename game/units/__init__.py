import pygame
import theme
from engine.units import GameObject
import Queue
import helpers
from helpers.timer import Timer
import random
import logging
import os
import math
from engine.units import Entity
from engine.units.components import EntityLink, Movable, Rotatable, SimpleRenderable
from engine.object_manager import BuildOrder
import units


class Test(Entity, EntityLink, Movable, Rotatable, SimpleRenderable):
    """Test

    Initial test entity.

    """
    name = 'The First One'

    vertices = [
        (-5, -5),
        (5, -5),
        (5, 5),
        (-5, 5),
    ]
    
    color = theme.red,
    count = 0

    def update(self, delta):
        # super(Test, self).update(delta)
        target_pos = self.link.get_target()
        d = helpers.get_direction(self.position, target_pos)
        self.move(d)
        self.face(target_pos)
        self.count += 1
        if self.count > 30:
            self.count = 0
            return [BuildOrder(units.Bullet, position=self.position, target=target_pos)]


class Bullet(Entity, EntityLink, Movable, Rotatable, SimpleRenderable):
    name = 'Bullet'
    
    vertices = [
        (-1, -10),
        (1, -10),
        (1, 10),
        (-1, 10),
    ]
    
    color = theme.blue,

    speed = 10

    def __init__(self, target, **kwargs):
        super(Bullet, self).__init__(**kwargs)
        self.face(target)

    def update(self, delta):
        dist = [self.speed * o for o in self.orientation]
        self.move(dist)


class Pulse(GameObject):
    """Pulse

    Shot by a pulse rilfe

    """
    speed = 1200.0

    def __init__(self, position, direction):
        super(Pulse, self).__init__('assets/pulse.png', position)
        self.direction = direction
        angle = (180.0/math.pi) * (math.atan((direction[0]/direction[1])))
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self, delta, **kwargs):
        dist = self.speed * delta
        dist_x = self.direction[0] * dist
        dist_y = self.direction[1] * dist
        self.move(dist_x, dist_y)
        return []

    def __str__(self):
        return 'Pulse'
        

class Bot(GameObject):
    """Bot

    Basic tier 1 unit.

    """

    fire_rate = 3.0
    fire_dist = 20
    movement_speed = 60.0 

    def __init__(self, position):
        super(Bot, self).__init__('assets/circle.png', position)
        self._fire_timer = Timer(Bot.fire_rate)

    def _fire(self, position):
        diff_x = position[0] - self.position[0]
        diff_y = position[1] - self.position[1]
        aim = helpers.normalize((diff_x, diff_y))
        l = Bot.fire_dist
        fire_pos = (self.position[0] + aim[0] * l, self.position[1] + aim[1] * l)
        return Pulse(position=fire_pos, direction=aim)
    
    def fire(self, position):
        if self._fire_timer.check():
            self._fire_timer.reset()
            return self._fire(position)
        return []

    def update(self, delta, **kwargs):
        self._fire_timer.update(delta)
        dist = Bot.movement_speed * delta
        self.move(dist, 0)
        targets = [(400, 400), (200, 200), (300, 300)]
        if targets:
            target = random.choice(targets)
            shot = self.fire(target)
        if shot:
            return [shot]
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