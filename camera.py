class Camera:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.roll = 0  # degrees
        self.scale_x = 1.0
        self.scale_y = 1.0

    def __repr__(self):
        return f'Camera({self.x}, {self.y})'
