

class Thing(object):

    def __init__(self, position):
        self.position = position

    def move(self, x, y):
        new_x = float(self.position[0]) + float(x)
        new_y = float(self.position[1]) + float(y)
        self.position = (int(new_x), int(new_y))

    def __str__(self):
        return 'Thing'