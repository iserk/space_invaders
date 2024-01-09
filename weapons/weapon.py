import random

import numpy as np
import pygame

from objects.position import Position


class Weapon:
    SPEED = 500
    SHOOT_DELAY = 200
    ACCURACY = 0.8

    CLIP_SIZE = 10
    RELOAD_TIME = 1000
    MAX_AMMO = 100

    def __init__(self, vehicle=None):
        self.name = self.__class__.__name__
        self.shot = None
        self.vehicle = vehicle
        self.prev_shot_time = 0
        self.clip = self.CLIP_SIZE
        self.ammo = self.MAX_AMMO

    def can_shoot(self):
        # return self.vehicle.scene.game.total_time - self.prev_shot_time > self.SHOOT_DELAY
        return self.get_charge() >= 1 and self.clip > 0

    def get_charge(self):
        # return (self.vehicle.scene.game.total_time - self.prev_shot_time) / self.SHOOT_DELAY
        return min(1, (self.vehicle.scene.game.total_time - self.prev_shot_time) / self.SHOOT_DELAY)

    def get_reload_time_left(self):
        return max(0, self.prev_shot_time + self.RELOAD_TIME - self.vehicle.scene.game.total_time)

    def _send_bullet(self, scene, pos, velocity):
        """Sends a single bullet with the given parameters."""
        return self.shot(
            scene, pos,
            # velocity + Position((np.random.default_rng().normal() - 0.5) * self.shot.SPEED * (1 - self.ACCURACY), 0)
            velocity + Position(random.uniform(-1, 1) * self.shot.SPEED * (1 - self.ACCURACY), 0)
        )

    def _perform_shot(self, scene, pos, velocity):
        """Performs a single shot with the given parameters."""
        self._send_bullet(scene, pos, velocity)

    def shoot(self, scene, pos, velocity):
        if not self.can_shoot():
            if self.clip <= 0:
                pygame.mixer.Sound(f"assets/audio/gatling/empty_clip.wav").play()
            return

        self._perform_shot(scene, pos, velocity)

        self.clip -= 1
        self.prev_shot_time = scene.game.total_time

    def reload(self, dt):
        self.clip = self.CLIP_SIZE
        self.ammo -= self.CLIP_SIZE
        if self.ammo < 0:
            self.clip += self.ammo
            self.ammo = 0

        self.prev_shot_time += self.RELOAD_TIME

    def update(self, dt):
        if self.clip <= 0:
            self.reload(dt)
