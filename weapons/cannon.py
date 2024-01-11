import random
import numpy as np

import pygame

from utils import audio
from utils.sprites import get_frames

from objects.invader_shot import InvaderShot
from objects.invader import Invader
from objects.position import Position
from objects.game_object import Sprite

from weapons.hero_shot import HeroWeapon, HeroShot

from scenes.scene import Scene
from weapons.shot import ShotState


class CannonShot(HeroShot):
    DAMAGE = 24
    SCORE_COST = DAMAGE
    DESTROY_ON_HIT = False

    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.1
    AGAINST_ARMOR = 1.25
    AGAINST_HULL = 0.75

    SHIELD_PIERCING = 0.25  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.25  # Percentage of initial damage that goes through to hull

    # SHOT_SIZE = (48, 48)

    def __init__(self, scene: Scene, pos: Position, velocity: Position, scale=2):
        # velocity += Position((np.random.default_rng().normal() - 0.5) * self.SPEED * (1 - self.ACCURACY), 0)

        super().__init__(scene, pos, velocity)

        self.scale = scale
        image = pygame.image.load("assets/images/cannon_shot.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 3),
            width=32 * scale,
            height=32 * scale,
        )


class Cannon(HeroWeapon):
    SPEED = 3000
    SHOOT_DELAY = 800
    PELLETS = 1
    ACCURACY = 0.8

    CLIP_SIZE = 1
    RELOAD_TIME = 1200
    MAX_AMMO = 20

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = CannonShot

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        audio.sound(f"assets/audio/cannon/shot{random.randint(1, 2):02}.wav", volume=3).play()
