

def handle_pointer(event, pointer):
    if event.type == 4:
        if pointer.down:
            print 'Pointer Drag'
        else:
            print 'Pointer Move'
    elif event.type == 5:
        if not pointer.down:
            pointer.down = True
            print 'Pointer Down'
    elif event.type == 6:
        if pointer.down:
            pointer.down = False
            print 'Pointer Up'


class Pointer(object):
    
    def __init__(self):
        self.down = False

