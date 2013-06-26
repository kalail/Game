import pygame
import collections
import entities.components as components
import pygame.locals as pylocals
import sys
# import time
import PAL
from .managers import InteractionManager, AssetManager, EventManager, EntityManager
from .renderer import OpenGLRenderer as Renderer


# class Pointer(GameObject):

#     def __init__(self, position=(0,0)):
#         super(Pointer, self).__init__('assets/cursor.png', position)

#     def update(self, delta):
#         new_position = PAL.get_pointer_position()
#         self.move(new_position[0]-self.position[0], new_position[1]-self.position[1])
#         return []


class Engine(object):
    """Engine

    Game engine that runs levels. Takes a configuration too.

    """
    def __init__(self, config, game_cls):
        """Setup engine components according to provided configuration and platform."""
        # Save inputs
        self.config = config
        self.game = game_cls()
        self.levels = collections.deque(self.game.levels)
        # Create first level
        level_cls = self.levels.popleft()
        self.level = level_cls()
        # Initialize Platform Abstracion Layer
        PAL.init()
        # Setup engine for level
        self.asset_manager = AssetManager(self.game.assets)
        self.entity_manager = EntityManager()
        self.renderer = Renderer(self)
        self.interaction_manager = InteractionManager()
        self.event_manager = EventManager()
        # Set timer
        self.game_timer = PAL.get_clock()

    def start(self):
        """Load level assets and start the main loop."""

        # Load level assets
        # for asset in self.level.assets:

        # Setup object lists
        # Setup level_specific engine modules
        # assets = [
        # ]
        # for a in asset
        # self.assets.
        self.asset_manager.load()
        self.renderer.start()
        self.renderer.compile_program()
        music = self.asset_manager.get('assets/ThisUsedToBeACity.ogg')
        self.ping = self.asset_manager.get('assets/beep.ogg')
        music.play()
        # self.pointer = Pointer()
        self.entity_manager.build_multiple(self.level.starting_order())
        self.run()

    def run(self):
        delta = 0
        while True:
            # Handle events
            # start = time.clock()
            # first = start
            self.handle_events(delta)
            # end = time.clock()
            # logging.debug('Handled events in: %ss' % (end - start))
            # Update world
            # start = time.clock()
            self.update(delta)
            # end = time.clock()
            # logging.debug('Updated world in: %ss' % (end - start))
            # Create new objects
            # start = time.clock()
            # end = time.clock()
            # logging.debug('Added %s new objects in: %ss' % (len(new_objects), (end-start)))
            # Run engine plugins
            # start = time.clock()
            if self.config.check_bounds:
                self.check_bounds()
                # print 'Culled %s out of bound objects' % num_culled
            # end = time.clock()
            # logging.debug('Ran engine plugins in: %ss' % (end - start))
            # Draw objects
            # start = time.clock()
            self.draw()
            # end = time.clock()
            # total = end - first
            # logging.debug('Rendered frame in: %ss\n' % (end - start))
            # Get ticks
            delta_millis = self.game_timer.tick(self.config.framerate)
            delta = float(delta_millis) / 1000.0
            # slept = delta - total
            # Calculate fps
            # trash = self._frame_times.get_nowait()
            # del trash
            # self._frame_times.put(delta)
            # times = [self._frame_times.get_nowait() for i in xrange(self._num_fps_avg)]
            # [self._frame_times.put(t) for t in times]
            # fps = 1.0 / (sum(times) / len(times))
            # logging.debug('Total processing time: %ss' % total)
            # logging.debug('Slept for: %ss' % slept)
            # logging.debug('Total frame time: %ss\n' % delta)

            # logging.debug('Estimated CPU Usage: %s%%' % (total/delta*100.0))
            # logging.debug('Estimated FPS: %s\n' % fps)
            # logging.debug('----------------------------------------------------------\n')

    def check_bounds(self):
        for e in self.entity_manager.entities:
            if isinstance(e, components.Movable):
                in_screen = ((0 < e.position[0] < self.renderer.width), (0 < e.position[1] < self.renderer.height))
                if False in in_screen:
                    self.entity_manager.remove(e)

    def handle_events(self, delta):
        events = self.event_manager.get()
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
        self.entity_manager.update(delta)

    def draw(self):
        self.renderer.clear()
        self.renderer.draw(self.entity_manager.entities)
        if self.config.debug:
            for i in self.interaction_manager.interactions[-3:]:
                if len(i.points) > 1:
                    pygame.draw.aalines(self.renderer.surface, (12,43,32), False, i.points)
                    for p in i.points:
                        pygame.draw.circle(self.renderer.surface, (10,50,10), p, 2)
        self.renderer.flip()

    def quit(self):
        PAL.quit()
        sys.exit()