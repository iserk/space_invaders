import random

from pygame import Vector2

from weapons.weapon import Weapon
from weapons.cannon_shot import CannonShot

import random
import numpy as np

import pygame

from objects.invader_shot import InvaderShot
from objects.shot import Shot
from objects.invader import Invader
from objects.position import Position
from objects.game_object import Sprite
from scenes.scene import Scene

from utils.sprites import get_frames


class LaserShot(Shot):
    SCORE_COST = 1
    DAMAGE = 2
    PULSE_DURATION = 500

    def __init__(self, scene: Scene, pos: Position, velocity: Position, weapon=None):
        super().__init__(scene, pos, velocity)

        self.weapon = weapon
        self.start_time = self.scene.game.total_time

        # self.scale = scale
        # image = pygame.image.load("assets/images/hero_shot.png").convert_alpha()
        # image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        #
        # self.sprite = Sprite(
        #     frames=get_frames(
        #         image, 32 * scale, 32 * scale, 3),
        #     width=32 * scale,
        #     height=32 * scale,
        # )

        # self.scene.game.traumatize(0.1)

        self.frame = 0
        self.scene.game.score -= self.SCORE_COST

    def draw(self, camera):
        # super().draw(camera)

        pygame.draw.line(
            camera.screen,
            (128, 128, 64),
            tuple(self.pos),
            tuple(self.pos + Position(0, -1000)),
            4
        )

        # # print(self.get_collider())
        # r = (
        #         min(self.get_rect()[0].x, self.get_rect()[1].x),
        #         min(self.get_rect()[0].y, self.get_rect()[1].y),
        #         abs(self.get_rect()[1].x - self.get_rect()[0].x),
        #         abs(self.get_rect()[1].y - self.get_rect()[0].y) + 2,
        #     )
        # print(__class__.__name__, r)
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
        super().update(dt)

        self.pos = self.scene.hero.pos.copy()

        if self.frame == 2:
            self.destroy()
            return

        if self.pos.y < 0 or self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()
            return

        if self.scene.game.total_time - self.start_time > self.PULSE_DURATION:
            self.destroy()
            return

        self.detect_collisions()

    def get_rect(self):
        return [
            Vector2(self.pos.x - 8, self.pos.y),
            Vector2(self.pos.x + 8, self.pos.y - 1000),
        ]

    def on_collision(self, obj=None):
        if isinstance(obj, Invader) or isinstance(obj, InvaderShot):
            self.scene.game.traumatize(0.2)
            obj.hit(damage=self.DAMAGE, by=self)
            if obj.hit_points <= 0:
                self.scene.game.score += obj.SCORE
            # self.frame = 2

    # def destroy(self):
    #     if self.weapon is not None and self.weapon.sound is not None:
    #         self.weapon.sound.stop()
    #     super().destroy()


class Laser(Weapon):
    SPEED = 1
    SHOOT_DELAY = 1800
    PELLETS = 1
    ACCURACY = 1

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = LaserShot
        self.sound = None

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity)

        sound = pygame.mixer.Sound(f"assets/audio/beam_shot.wav").play()
        self.vehicle.scene.add_timer(500, lambda: sound.fadeout(500) if sound is not None else None)


