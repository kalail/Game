import pygame
import input_manager
import units
import pygame.locals as pylocals
import theme
import sys
import base
import time
import Queue
import logging
import random


class Engine(object):
    """Engine

    Powers the game. Built on pygame.

    """
    def __init__(self, config):
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode(self.config.size)
        pygame.display.set_caption(self.config.title)
        self.timer = pygame.time.Clock()
        self.input_manager = input_manager.InputManager()
        self.objects = [units.Home(side='left', color=theme.red, rate=10, build_queue=[units.Bot for i in xrange(100)])]
        self._num_fps_avg = 5
        self._frame_times = Queue.Queue(self._num_fps_avg)
        [self._frame_times.put(0) for i in xrange(self._num_fps_avg)]

    def start(self):
        self.run()

    def run(self):
        delta = 0
        while True:
            start = time.clock()
            first = start
            # Handle events
            self.handle_events(delta)
            end = time.clock()
            logging.info('Handled events in: %ss' % (end - start))
            # Update world
            start = time.clock()
            new_objects = self.update(delta)
            end = time.clock()
            logging.info('Updated world in: %ss' % (end - start))
            # Create new objects
            start = time.clock()
            self.objects.extend(new_objects)
            end = time.clock()
            logging.info('Added %s new objects in: %ss' % (len(new_objects), (end-start)))
            # Run engine plugins
            start = time.clock()
            if self.config.check_bounds:
                num_culled = self.check_bounds()
                logging.info('Culled %s out of bound objects' % num_culled)
            end = time.clock()
            logging.info('Ran engine plugins in: %ss' % (end - start))
            # Draw objects
            start = time.clock()
            self.draw()
            end = time.clock()
            total = end - first
            logging.info('Rendered frame in: %ss\n' % (end - start))
            # Get ticks
            delta_millis = self.timer.tick(self.config.framerate)
            delta = float(delta_millis) / 1000.0
            slept = delta - total
            # Calculate fps
            trash = self._frame_times.get_nowait()
            del trash
            self._frame_times.put(delta)
            times = [self._frame_times.get_nowait() for i in xrange(self._num_fps_avg)]
            [self._frame_times.put(t) for t in times]
            fps = 1.0 / (sum(times) / len(times))
            logging.info('Total processing time: %ss' % total)
            logging.info('Slept for: %ss' % slept)
            logging.info('Total frame time: %ss\n' % delta)

            logging.info('Estimated CPU Usage: %s%%' % (total/delta*100.0))
            logging.info('Estimated FPS: %s\n' % fps)
            logging.info('----------------------------------------------------------\n')
    def check_bounds(self):
        count = 0
        for o in self.objects:
            if isinstance(o, base.Thing):
                in_screen = ((0 < o.position[0] < self.config.width), (0 < o.position[1] < self.config.height))
                if False in in_screen:
                    self.objects.remove(o)
                    count += 1
        return count

    def handle_events(self, delta):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pylocals.QUIT:
                self.quit()
            # else:
                # interactions = self.input_manager.handle_input(event, delta)
                # handle interactions

    def update(self, delta):
        new_objects = []
        for o in self.objects:
            possible_objects = o.update(delta, command_link=self)
            if possible_objects:
                new_objects.append(possible_objects)
        flat = []
        [flat.extend(objects) for objects in new_objects]
        return flat

    def draw(self):
        self.screen.fill(theme.white)
        # pygame.draw.rect(self.screen, theme.blue,  (10, 10, 10, 10))
        for o in self.objects:
            o.draw(self.screen)
        pygame.display.update()

    def within_range(self, target):
        x = 530 + random.random() * 40
        y = 280 + random.random() * 40
        return [base.Thing(position=(x, y))]

    def quit(self):
        pygame.quit()
        sys.exit()