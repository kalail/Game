class Drag(Interaction):

    def __init__(self, position=None):
        super(Drag, self).__init__(position)
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