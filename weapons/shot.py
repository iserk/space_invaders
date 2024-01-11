import random
from enum import Enum

import pygame.draw
from pygame import Vector2

from objects.explodable_rigid_body import ExplodableRigidBody
from objects.position import Position
from scenes.scene import Scene


class ShotState(Enum):
    STARTING = 0
    FLYING = 1
    HITTING = 2
    DESTROYED = 3


class Shot(ExplodableRigidBody):
    DAMAGE = 1
    SHOT_LENGTH = 16
    DESTROY_ON_HIT = True
    SPEED = 500
    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.1
    AGAINST_ARMOR = 0.5
    AGAINST_HULL = 1

    SHIELD_PIERCING = 0.0  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.0  # Percentage of initial damage that goes through to hull

    SHOT_SIZE = (16, 16)

    def __init__(self, scene: Scene, pos: Position, velocity: Position):
        super().__init__(scene, pos, None)
        self.pos = pos
        self.velocity = velocity

        self.direction = self.velocity.get_normalized() * Shot.SHOT_LENGTH

        self.damage = self.DAMAGE

        self.state = ShotState.STARTING
        self.frame = self.state2frame()

    def state2frame(self):
        match self.state:
            case ShotState.STARTING:
                return 0
            case ShotState.FLYING:
                return 1
            case ShotState.HITTING:
                return 2
            case ShotState.DESTROYED:
                return 2

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

        if self.state == ShotState.STARTING:
            self.state = ShotState.FLYING
            self.frame = self.state2frame()

    def update(self, dt):
        # Forces the shoot to display the 0 frame from the start position
        # by avoiding movement on the first frame
        if self.state != ShotState.STARTING:
            super().update(dt)

        if self.state == ShotState.DESTROYED:
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
