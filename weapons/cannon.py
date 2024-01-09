import random

import pygame

from weapons.weapon import Weapon
from weapons.cannon_shot import CannonShot


class Cannon(Weapon):
    SPEED = 3000
    SHOOT_DELAY = 600
    PELLETS = 1
    ACCURACY = 0.8

    CLIP_SIZE = 10
    RELOAD_TIME = 1000
    MAX_AMMO = 100

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = CannonShot

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        pygame.mixer.Sound(f"assets/audio/cannon/shot{random.randint(1, 2):02}.wav").play()
