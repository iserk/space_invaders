class Timer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.start_time = 0
        self.is_running = True

    def __repr__(self):
        return f'Timer({self.interval}, {self.callback})'

    def update(self, dt):
        if not self.is_running:
            return

        self.start_time += dt
        if self.start_time >= self.interval:
            print('timer done: ', self)
            self.start_time = 0
            self.callback()
            self.is_running = False
