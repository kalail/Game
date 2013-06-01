import pygame.locals as pylocals
import logging


# class VectorInteration(Interaction):
#     pass

# class ScalarInteration(Interaction):
#     pass

# class Drag(VectorInteration):
#     pass

# class Tap(ScalarInteration):
#     pass

class MouseInput(object):
    
    def __init__(self, tap_delay=0.04):
        self.down = False
        self._new_drag = None
        self._new_tap = None
        # self.tap_delay = tap_delay
        # self._delay_timer = 0.0

    # def _get_touch_id(self):
    #     pass

    # def _new_touch_id(self):
    #     return len(self.touches)

    def _start_interaction(self, position):
        drag = Drag(position)
        tap = Tap(position)
        self._new_tap = tap
        self._new_drag = drag
        self.down = True
        self.interaction = None

    def _finish_interaction(self, position):
        if self.interaction:
            i = self.interaction
            assert i.name == 'drag'
            i.points.append(position)
        else:
            i = self._new_tap
            self._new_tap = None
            self._new_drag = None
            assert i.name == 'tap'
            if i.position == position:
                pass
            else:
                i = None
        print i
        self.down = False
        return i

    def _choose_drag(self, position):
        drag = self._new_drag
        if drag:
            drag.points.append(position)
            self.interaction = drag
        self._new_drag = None
        self._new_tap = None

    def handle_input(self, event, delta):
        # self._delay_timer += delta
        if event.type == pylocals.MOUSEMOTION:
            if self.down:
                self._choose_drag(event.pos)
            # else:
                # print 'Pointer Move'
        elif event.type == pylocals.MOUSEBUTTONDOWN:
            if not self.down:
                if event.button == 1:
                    self._start_interaction(event.pos)
        elif event.type == pylocals.MOUSEBUTTONUP:
            if self.down:
                if event.button == 1:
                    touch = self._finish_interaction(event.pos)
                    if touch:
                        return [touch]
        return None


class InputManager(MouseInput):

    def __init__(self, *args, **kwargs):
        super(InputManager, self).__init__(*args, **kwargs)
        self.interaction = None


import os


class Interaction(object):
    def __init__(self, position, key=None):
        if not key:
            key = self._create_random_key()
        self.key = key
        self.points = []
        self.points.append(position)
        self.lifetime = 0.0
        self.complete = False

    def add_point(self, position):
        self.points.append(position)

    def end(self, position):
        self.points.append(position)
        self.complete = True

    def _create_random_key(self):
        return os.urandom(16).encode('hex')

class InteractionManager(object):

    @staticmethod
    def pc_create_interaction(event, interactions):
        key = event.button
        i = Interaction(event.pos, key)
        interactions.append(i)

    @staticmethod
    def pc_update_interactions(event, interactions):
        for key, conditional in enumerate(event.buttons):
            key += 1
            if conditional:
                interaction = None
                for i in interactions:
                    if not i.complete:
                        if i.key == key:
                            interaction = i
                if interaction:
                    interaction.add_point(event.pos)

    @staticmethod
    def pc_end_interaction(event, interactions):
        key = event.button
        for i in interactions:
            if not i.complete:
                if i.key == key:
                    interaction = i
        interaction.end(event.pos)

    def __init__(self):
        self.interactions = []

    def update(self, events, delta):
        for i in self.interactions:
            i.lifetime += delta
        for event in events:
            t = event.type
            if t == pylocals.MOUSEBUTTONDOWN:
                self._create_interaction(event)
            elif t == pylocals.MOUSEMOTION:
                self._update_interactions(event)
            elif t == pylocals.MOUSEBUTTONUP:
                self._end_interaction(event)

    def _create_interaction(self, event):
        InteractionManager.pc_create_interaction(event, self.interactions)

    def _update_interactions(self, event):
        InteractionManager.pc_update_interactions(event, self.interactions)

    def _end_interaction(self, event):
        InteractionManager.pc_end_interaction(event, self.interactions)

