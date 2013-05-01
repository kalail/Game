import pygame
from .input_manager import InteractionManager
import units
import pygame.locals as pylocals
import theme
import sys
import time
import Queue
import logging
from .object_manager import ObjectManager

class Renderer(object):
    def __init__(self, adapter, resolution, fullscreen, clear_color):
        self.adapter = adapter
        self.clear_color = clear_color
        self.surface = adapter.create_surface(resolution, fullscreen)

    def clear(self):
        self.adapter.clear(self.surface, self.clear_color)

    def flip(self):
        self.adapter.flip()



class Engine(object):
    """Engine

    Powers the game. Built on pygame.

    """
    def __init__(self, config, adapter_class):
        # Initialize
        self.adapter = adapter_class()
        # Save config
        self.config = config
        # Create screen
        self.renderer = Renderer(self.adapter, config.resolution, config.fullscreen, theme.white)
        # Set timeout
        self.timer = self.adapter.get_clock()
        self.interaction_manager = InteractionManager()
        # objects = [units.Home(side='left', color=theme.red, rate=10, build_queue=[units.Bot for i in xrange(100)])]
        objects = [
            units.Bot((25, 25)),
            units.Bot((45, 25)),
            units.Bot((25, 45)),
        ]
        self.object_manager = ObjectManager(objects)
        self._num_fps_avg = 5
        self._frame_times = Queue.Queue(self._num_fps_avg)
        [self._frame_times.put(0) for i in xrange(self._num_fps_avg)]
        self.target = (500, 200)

    def start(self):
        music = self.adapter.load_sound('assets/ThisUsedToBeACity.ogg')
        self.ping = self.adapter.load_sound('assets/ping.wav')
        music.play()
        self.pointer = units.Pointer(self.adapter)
        self.object_manager.add(self.pointer)
        self.run()

    def run(self):
        delta = 0
        while True:
            # Handle events
            start = time.clock()
            first = start
            self.handle_events(delta)
            end = time.clock()
            logging.debug('Handled events in: %ss' % (end - start))
            # Update world
            start = time.clock()
            new_objects = self.update(delta)
            end = time.clock()
            logging.debug('Updated world in: %ss' % (end - start))
            # Create new objects
            start = time.clock()
            self.object_manager.add(new_objects)
            end = time.clock()
            logging.debug('Added %s new objects in: %ss' % (len(new_objects), (end-start)))
            # Run engine plugins
            start = time.clock()
            if self.config.check_bounds:
                num_culled = self.check_bounds()
                logging.debug('Culled %s out of bound objects' % num_culled)
            end = time.clock()
            logging.debug('Ran engine plugins in: %ss' % (end - start))
            # Draw objects
            start = time.clock()
            self.draw()
            end = time.clock()
            total = end - first
            logging.debug('Rendered frame in: %ss\n' % (end - start))
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
            logging.debug('Total processing time: %ss' % total)
            logging.debug('Slept for: %ss' % slept)
            logging.debug('Total frame time: %ss\n' % delta)

            logging.debug('Estimated CPU Usage: %s%%' % (total/delta*100.0))
            logging.debug('Estimated FPS: %s\n' % fps)
            logging.debug('----------------------------------------------------------\n')

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
        events = pygame.event.get()
        self.interaction_manager.update(events, delta)
        for event in events:
            if event.type == pylocals.QUIT:
                self.quit()
            elif event.type == pylocals.KEYDOWN:
               if event.key == pylocals.K_ESCAPE:
                   self.quit()
            elif event.type == pylocals.MOUSEBUTTONDOWN:
                self.ping.play()

    def update(self, delta):
        new_objects = self.object_manager.update(delta)
        return new_objects

    def draw(self):
        self.renderer.clear()
        self.object_manager.draw(self.renderer.surface)
        if self.config.debug:
            for i in self.interaction_manager.interactions[-3:]:
                if len(i.points) > 1:
                    pygame.draw.aalines(self.renderer.surface, (12,43,32), False, i.points)
                    for p in i.points:
                        pygame.draw.circle(self.renderer.surface, (10,50,10), p, 2)
        self.renderer.flip()

    def quit(self):
        self.adapter.quit()
        sys.exit()