import random

import pygame

from weapons.shotgun_shot import ShotgunShot
from weapons.weapon import Weapon
from weapons.cannon_shot import CannonShot


class Shotgun(Weapon):
    SPEED = 1000
    SHOOT_DELAY = 2000
    PELLETS = 20

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = ShotgunShot

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        pygame.mixer.Sound(f"assets/audio/gatling/shot{random.randint(1,3):02}.wav").play()
