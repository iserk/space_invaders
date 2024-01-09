import pygame


class Camera:
    def __init__(self, screen_size, x, y):
        self.screen_size = screen_size
        self.screen = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.roll = 0  # degrees
        self.scale_x = 1.0
        self.scale_y = 1.0

    def __repr__(self):
        return f'Camera({self.x}, {self.y})'

    def display(self, screen):
        temp_screen = self.screen

        if self.roll != 0:
            temp_screen = pygame.transform.rotate(self.screen, self.roll)

        if self.scale_x != 1 or self.scale_y != 1:
            temp_screen = pygame.transform.scale(temp_screen, (
                self.screen_size[0] * self.scale_x, self.screen_size[1] * self.scale_y))

        screen.blit(temp_screen, (-self.x, -self.y))

    def shake(self, vector):
        print("Shaking camera", vector)
        self.x += vector.x
        self.y += vector.y
