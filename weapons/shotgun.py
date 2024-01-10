import random

import pygame

from utils import audio

from objects.invader_shot import InvaderShot
from objects.invader import Invader
from objects.position import Position
from objects.game_object import Sprite

from weapons.hero_shot import HeroWeapon, HeroShot

from scenes.scene import Scene

from utils.sprites import get_frames


class ShotgunShot(HeroShot):
    SCORE_COST = 2
    DAMAGE = 1
    SHOT_LENGTH = 16
    SPEED = 500
    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.1
    AGAINST_ARMOR = 0.5
    AGAINST_HULL = 1.75

    SHIELD_PIERCING = 0.05  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.10  # Percentage of initial damage that goes through to hull

    def __init__(self, scene: Scene, pos: Position, velocity: Position, scale=1):
        # velocity += Position((np.random.default_rng().normal() - 0.5) * self.SPEED * (1 - self.ACCURACY), 0)

        super().__init__(scene, pos, velocity)

        self.scale = scale
        image = pygame.image.load("assets/images/shotgun_shot.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 3),
            width=32 * scale,
            height=32 * scale,
        )


class Shotgun(HeroWeapon):
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
