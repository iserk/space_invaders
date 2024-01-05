class Camera:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Camera({self.x}, {self.y})'