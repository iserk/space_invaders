import random

import numpy as np

from pygame import Vector2

from utils import audio
from weapons.shot import Shot


class Weapon:
    SHOOT_DELAY = 200
    ACCURACY = 0.8

    PELLETS = 1

    CLIP_SIZE = 10
    RELOAD_TIME = 1000
    MAX_AMMO = 100

    RECOIL_FACTOR = 5

    def __init__(self, vehicle=None):
        self.shot = None
        self.vehicle = vehicle
        self.prev_shot_time = 0
        self.reloading_start_time = 0
        self.is_reloading = False
        self.empty_clip_sound_played = False

        self.clip = self.CLIP_SIZE
        self.ammo = self.MAX_AMMO

        self.shot = Shot

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.__class__.__name__

    def get_charge(self):
        # return (self.vehicle.scene.game.total_time - self.prev_shot_time) / self.SHOOT_DELAY
        return min(1, (self.vehicle.scene.game.total_time - self.prev_shot_time) / self.SHOOT_DELAY)

    def get_reload_time_left(self):
        return self.RELOAD_TIME + self.reloading_start_time - self.vehicle.scene.game.total_time

    def can_shoot(self):
        # return self.vehicle.scene.game.total_time - self.prev_shot_time > self.SHOOT_DELAY
        return self.get_charge() >= 1 and self.clip > 0 and not self.is_reloading

    def _send_bullet(self, scene, pos, velocity):
        """Sends a single bullet with the given parameters."""
        p = pos.copy()
        dispersion = self.shot.SPEED * (1 - self.ACCURACY)
        return self.shot(
            scene, p,
            # Normal distribution
            velocity + Vector2((np.random.default_rng().normal(0, dispersion)), 0)

            # Uniform distribution
            # velocity + Position(random.uniform(-1, 1) * self.shot.SPEED * (1 - self.ACCURACY), 0)
        )

    def _perform_shot(self, scene, pos, velocity):
        """Performs a single shot with the given parameters."""
        for _ in range(self.PELLETS):
            self._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        recoil_force = self.RECOIL_FACTOR * self.shot.MASS * self.PELLETS

        self.vehicle.scene.camera.displace(Vector2(0, -1) * min(64, recoil_force), 0)
        # trauma = 0.1 * self.shot.MASS * self.PELLETS
        trauma = 0.05 * recoil_force
        max_trauma = trauma * 2
        self.vehicle.scene.game.traumatize(trauma, max_trauma)

    def shoot(self, scene, pos, velocity):
        if not self.can_shoot():
            if self.clip <= 0 and not self.empty_clip_sound_played:
                audio.sound(f"assets/audio/empty_clip.wav").play()
                self.empty_clip_sound_played = True
            return

        self._perform_shot(scene, pos, velocity)
        # self.vehicle.scene.camera.shake(Vector2(0, 1) * self.RECOIL * 100)

        self.clip -= 1
        self.prev_shot_time = scene.game.total_time

    def stop_shooting(self):
        self.empty_clip_sound_played = False

    def start_reloading(self):
        if self.is_reloading:
            return
        self.is_reloading = True
        self.reloading_start_time = self.vehicle.scene.game.total_time
        # Play sound effect assets/audio/weapon_switch.wav
        audio.sound("assets/audio/weapon_switch.wav").play()

    def _reload(self):
        self.ammo -= self.CLIP_SIZE - self.clip
        self.clip = self.CLIP_SIZE
        if self.ammo < 0:
            self.clip += self.ammo
            self.ammo = 0

        self.is_reloading = False
        audio.sound(f"assets/audio/reload.wav").play()
        self.empty_clip_sound_played = True

    def update(self, dt):
        # print(self.name, self.clip, self.ammo, self.is_reloading, self.reloading_start_time)
        if self.clip <= 0 < self.ammo and not self.is_reloading:
            self.start_reloading()

        if (self.is_reloading
                and self.get_reload_time_left() <= 0
                and (self.ammo > 0 and self.clip < self.CLIP_SIZE or self.clip > 0)):
            self._reload()
