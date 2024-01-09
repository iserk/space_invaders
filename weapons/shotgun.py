import random

import pygame

from utils import audio
from weapons.shotgun_shot import ShotgunShot
from weapons.weapon import Weapon
from weapons.cannon_shot import CannonShot


class Shotgun(Weapon):
    SPEED = 1000
    PELLETS = 30
    ACCURACY = 0.6

    CLIP_SIZE = 4
    RELOAD_TIME = 2500
    SHOOT_DELAY = 800
    MAX_AMMO = 20

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = ShotgunShot

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        audio.sound(f"assets/audio/gatling/shot{random.randint(1,3):02}.wav").play()
