import pygame.locals as pylocals


class Interaction(object):
    pass

class VectorInteration(Interaction):
    pass

class ScalarInteration(Interaction):
    pass

class Drag(VectorInteration):
    pass

class Tap(ScalarInteration):
    pass


class MouseInput(object):
    
    def __init__(self, tap_delay=0.04):
        self.down = False
        self.tap_delay = tap_delay
        self._delay_timer = 0.0

    # def _get_touch_id(self):
    #     pass

    # def _new_touch_id(self):
    #     return len(self.touches)

    # def start_touch(self):
    #     touch = None
    #     self.touches.append(touch)

    # def update_touch(self):
    #     touch = False
    #     self.touches.append(touch)

    def handle_input(self, event, delta):
        self._delay_timer += (delta / 1000.0)
        if event.type == pylocals.MOUSEMOTION:
            if self.down:
                print 'Pointer Drag'
                self.update_touch()
            # else:
                # print 'Pointer Move'
        elif event.type == pylocals.MOUSEBUTTONDOWN:
            if not self.down:
                self.down = True
                if event.button == 1:
                    print 'Pointer Down'
                    self._delay_timer = 0.0
                    # self.start_touch()
        elif event.type == pylocals.MOUSEBUTTONUP:
            if self.down:
                self.down = False
                if event.button == 1:
                    print 'Pointer Up'
                    self.finish_touch()
        return None


class InputManager(MouseInput):

    def __init__(self, *args, **kwargs):
        super(InputManager, self).__init__(*args, **kwargs)
        self.touches = []

    def handle_input(self):
        pass