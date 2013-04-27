import pygame
import input_manager
import units
from units.base import Thing
import pygame.locals as pylocals
import theme
import sys
import time
import Queue
import logging
import random
from screen_manager import ScreenManager
from object_manager import ObjectManager

class Engine(object):
    """Engine

    Powers the game. Built on pygame.

    """
    def __init__(self, config):
        # Initialize
        pygame.init()
        # Save config
        self.config = config
        # Create screen
        self.screen_manager = ScreenManager(config.size, config.fullscreen)
        self.screen = self.screen_manager.screen
        # Set title
        pygame.display.set_caption(self.config.title)
        # Set timeout
        self.timer = pygame.time.Clock()
        self.input_manager = input_manager.InputManager()
        # objects = [units.Home(side='left', color=theme.red, rate=10, build_queue=[units.Bot for i in xrange(100)])]
        objects = [units.Bot((10, i*30)) for i in xrange(100)]
        self.object_manager = ObjectManager(objects)
        self._num_fps_avg = 5
        self._frame_times = Queue.Queue(self._num_fps_avg)
        [self._frame_times.put(0) for i in xrange(self._num_fps_avg)]
        self.target = (500, 200)

    def start(self):
        self.run()

    def run(self):
        delta = 0
        while True:
            # Handle events
            start = time.clock()
            first = start
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
            self.object_manager.add(new_objects)
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
        pass
        return 0
        # count = 0
        # for o in self.objects:
        #     if isinstance(o, Thing):
        #         in_screen = ((0 < o.position[0] < self.config.width), (0 < o.position[1] < self.config.height))
        #         if False in in_screen:
        #             self.objects.remove(o)
        #             count += 1
        # return count

    def handle_events(self, delta):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pylocals.QUIT:
                self.quit()
            elif event.type == pylocals.KEYDOWN:
               if event.key == pylocals.K_ESCAPE:
                   self.quit()
            else:
                interactions = self.input_manager.handle_input(event, delta)
                if interactions:
                    for i in interactions:
                        if i.name == 'drag':
                            pass
                        elif i.name == 'tap':
                            self.target = (i.position[0], i.position[1])
                            # self.input_manager.drags.extend(drags)
                            pass

    def update(self, delta):
        new_objects = self.object_manager.update(delta)
        return new_objects

    def draw(self):
        self.screen.fill(theme.white)
        self.object_manager.draw(self.screen)
        pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()