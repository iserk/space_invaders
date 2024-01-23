import pygame
from pygame import Vector2

from objects.displaceable_object import DisplaceableObject


class Camera(DisplaceableObject):
    def __init__(self, screen_size, pos: Vector2, displacement: Vector2 = Vector2(0, 0)):
        super().__init__(pos, displacement)
        self.screen_size = screen_size
        self.screen = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.pos = pos
        self.roll = 0  # degrees
        self.scale_x = 1.0
        self.scale_y = 1.0

    def __repr__(self):
        return f'Camera({self.pos}, {self.displacement})'

    def display(self, screen):
        temp_screen = self.screen

        if self.roll != 0:
            temp_screen = pygame.transform.rotate(self.screen, self.roll)

        if self.scale_x != 1 or self.scale_y != 1:
            temp_screen = pygame.transform.scale(temp_screen, (
                self.screen_size[0] * self.scale_x, self.screen_size[1] * self.scale_y))

        screen.blit(temp_screen, (-self.pos.x, -self.pos.y))

    def shake(self, vector):
        print("Shaking camera", vector)
        # self.pos += vector
        self.displacement = vector

