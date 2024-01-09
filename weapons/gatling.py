import random

from utils import audio
from weapons.weapon import Weapon
from weapons.gatling_shot import GatlingShot


class Gatling(Weapon):
    SPEED = 3000
    SHOOT_DELAY = 50
    PELLETS = 1
    ACCURACY = 0.7

    CLIP_SIZE = 50
    RELOAD_TIME = 1500
    MAX_AMMO = 200

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = GatlingShot

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        audio.sound(f"assets/audio/gatling/shot{random.randint(1,4):02}.wav").play()
