import pygame

from objects.game_object import GameObject
from objects.position import Position
from scenes.scene import Scene


class Shot(GameObject):
    SHOT_LENGTH = 16
    SPEED = 300

    def __init__(self, scene: Scene, pos: Position, velocity: Position, color: tuple):
        super().__init__(scene)
        self.pos = pos
        self.velocity = velocity
        self.color = color

        self.direction = self.velocity.get_normalized() * Shot.SHOT_LENGTH

    def draw(self, camera):
        pygame.draw.line(camera.screen, self.color, tuple(self.pos), tuple(self.pos + self.direction), 3)

    def update(self, dt):
        self.pos += self.velocity * dt / 1000

        if self.pos.y < 0 or self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()

