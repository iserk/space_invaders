import random

import pygame.draw
from pygame import Vector2

from objects.explodable_rigid_body import ExplodableRigidBody
from objects.position import Position
from scenes.scene import Scene


class Shot(ExplodableRigidBody):
    DAMAGE = 1
    SHOT_LENGTH = 16
    SPEED = 500
    SHOT_SIZE = (16, 16)

    def __init__(self, scene: Scene, pos: Position, velocity: Position):
        super().__init__(scene, pos, None)
        self.pos = pos
        self.velocity = velocity

        self.frame = 0

        self.direction = self.velocity.get_normalized() * Shot.SHOT_LENGTH

        self.damage = self.DAMAGE

    def draw(self, camera):
        super().draw(camera)
        #
        # pygame.draw.line(
        #     camera.screen,
        #     (128, 128, 128),
        #     tuple(self.prev_pos),
        #     tuple(self.pos),
        #     1
        # )

        # pygame.draw.rect(
        #     camera.screen,
        #     (255, 0, 0),
        #     (
        #         self.pos.x - self.sprite.width / 2,
        #         self.pos.y - self.sprite.height / 2,
        #         self.sprite.width,
        #         self.sprite.height,
        #     ),
        #     1
        # )
        # r = (
        #     min(self.get_collider()[0].x, self.get_collider()[2].x),
        #     min(self.get_collider()[0].y, self.get_collider()[2].y),
        #     abs(self.get_collider()[2].x - self.get_collider()[0].x),
        #     abs(self.get_collider()[2].y - self.get_collider()[0].y) + 2,
        # )
        #
        # # Draw red box around the collider
        # pygame.draw.rect(
        #     camera.screen,
        #     (255, 0, 0),
        #     r,
        #     1
        # )

        if self.frame == 0:
            self.frame = 1

    def update(self, dt):
        # Forces the shoot to display the 0 frame from the start position
        if self.frame == 1:
            super().update(dt)

        if self.frame == 2:
            self.destroy()
            return

        if self.pos.y < 0 or self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()

    def get_collider(self):
        return [
            Vector2(self.pos.x - self.SHOT_SIZE[0] / 2, self.pos.y - self.SHOT_SIZE[1] / 2),
            Vector2(self.pos.x + self.SHOT_SIZE[0] / 2, self.pos.y - self.SHOT_SIZE[1] / 2),
            Vector2(self.pos.x + self.SHOT_SIZE[0] / 2, self.pos.y + self.SHOT_SIZE[1] / 2),
            Vector2(self.pos.x - self.SHOT_SIZE[0] / 2, self.pos.y + self.SHOT_SIZE[1] / 2),
        ]
        # return [
        #     Vector2(self.prev_pos.x - self.SHOT_SIZE[0] / 2, self.prev_pos.y),
        #     Vector2(self.prev_pos.x + self.SHOT_SIZE[0] / 2, self.prev_pos.y),
        #     Vector2(self.pos.x + self.SHOT_SIZE[0] / 2, self.pos.y),
        #     Vector2(self.pos.x - self.SHOT_SIZE[0] / 2, self.pos.y),
        # ]

    @staticmethod
    def get_detonation_delay():
        return random.randint(20, 100)
