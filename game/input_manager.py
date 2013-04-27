import pygame.locals as pylocals
import logging

class Interaction(object):
    pass

# class VectorInteration(Interaction):
#     pass

# class ScalarInteration(Interaction):
#     pass

# class Drag(VectorInteration):
#     pass

# class Tap(ScalarInteration):
#     pass

class Drag(Interaction):

    def __init__(self, position=None):
        self.name = 'drag'
        self.points = []
        if position:
            self.points.append(position)

    def __str__(self):
        return self.name

class Tap(Interaction):

    def __init__(self, position=None):
        self.name = 'tap'
        self.position = position

    def __str__(self):
        # logging.error('(%s, %s)' % (self.position[0], self.position[1]))
        return self.name

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
