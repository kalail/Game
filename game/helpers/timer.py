

class Timer(object):
    def __init__(self, rate):
        self.rate = float(rate)
        self.period = 1.0 / rate
        self._count = self.period

    def tick(self, delta):
        self.update(delta)
        return self.check()

    def check(self):
        if self._count < self.period:
            return False
        return True

    def update(self, delta):
        if not self.check():
            self._count += delta

    def reset(self):
        self._count = 0.0


class TimerSet(object):
    def __init__(self, rates):
        self.timers = [Timer(rate) for rate in rates]

    def update(self, delta):
        for timer in self.timers:
            timer.update(delta)
