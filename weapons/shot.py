import random
from enum import Enum

import pygame
from pygame import Vector2

from objects.explodable_rigid_body import ExplodableRigidBody
from scenes.scene import Scene


class ShotState(Enum):
    STARTING = 0
    FLYING = 1
    HITTING = 2
    DESTROYED = 3


class Shot(ExplodableRigidBody):
    WINDAGE = 0.01
    MASS = 0.1
    SPEED = 1000
    DAMAGE = 100
    DETONATION_CHANCE = 0.0

    DESTROY_ON_HIT = False
    CRITICAL_HIT_CHANCE = 0.1
    RICOCHET_CHANCE = 0.3
    RICOCHET_DAMAGE_PERCENTAGE = 0.75   # Percentage of initial velocity that remains after ricochet

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.1
    AGAINST_ARMOR = 0.5
    AGAINST_HULL = 1

    SHIELD_PIERCING = 0.0  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.0  # Percentage of initial damage that goes through to hull

    SHOT_SIZE = (16, 16)

    def __init__(self, scene: Scene, pos: Vector2, velocity: Vector2):
        super().__init__(scene, pos, None)
        self.pos = pos
        self.velocity = velocity

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

        # pygame.draw.line(
        #     camera.screen,
        #     (128, 128, 128),
        #     tuple(self.prev_pos),
        #     tuple(self.pos),
        #     1
        # )
        #
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

        # r =self.get_rect()
        #
        # # Draw red box around the collider
        # pygame.draw.rect(
        #     camera.screen,
        #     (0, 255, 255),
        #     # self.get_rect(),
        #     (
        #         r[0].x,
        #         r[0].y,
        #         r[1].x - r[0].x,
        #         r[1].y - r[0].y,
        #     ),
        #     1
        # )

        if self.state == ShotState.STARTING:
            self.state = ShotState.FLYING
            self.frame = self.state2frame()

        if self.state == ShotState.HITTING:
            self.state = ShotState.FLYING
            self.frame = self.state2frame()

    def update(self, dt):
        # Forces the shoot to display the 0 frame from the start position
        # by avoiding movement on the first frame
        if self.state == ShotState.HITTING and not self.DESTROY_ON_HIT:
            self.state = ShotState.FLYING
            self.frame = self.state2frame()

        if self.state != ShotState.STARTING:
            super().update(dt)

        if (self.state == ShotState.DESTROYED
                or self.pos.y < 0
                or self.pos.y > self.scene.game.screen_size[1]
                or self.pos.x < 0
                or self.pos.x > self.scene.game.screen_size[0]
                or self.velocity.length() < 10
        ):
            self.destroy()
            return

    def get_rect(self):
        # return [
        #     Vector2(self.pos.x - self.sprite.width / 2, self.pos.y - self.sprite.height / 2),
        #     Vector2(self.pos.x + self.sprite.width / 2, self.pos.y + self.sprite.height / 2),
        # ]

        return (
                Vector2(self.pos.x - self.SHOT_SIZE[0] / 2, self.pos.y - self.SHOT_SIZE[1] / 2),
                Vector2(self.pos.x + self.SHOT_SIZE[0] / 2, self.pos.y + self.SHOT_SIZE[1] / 2),
        )

    @staticmethod
    def get_detonation_delay():
        return random.randint(20, 100)

    def speed2damage(self, speed):
        return self.DAMAGE * speed / self.SPEED

    def damage2speed(self, damage):
        return self.SPEED * damage / self.DAMAGE

    def get_damage(self):
        return self.DAMAGE * self.velocity.length() / self.SPEED
