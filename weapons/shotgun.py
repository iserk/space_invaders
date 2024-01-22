import random

import pygame
from pygame import Vector2

from utils import audio

from objects.game_object import Sprite

from weapons.hero_shot import HeroWeapon, HeroShot

from scenes.scene import Scene

from utils.sprites import get_frames


class ShotgunShot(HeroShot):
    WINDAGE = 0.002
    MASS = 0.1
    SPEED = 1200
    DAMAGE = 8
    SCORE_COST = DAMAGE
    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.001
    AGAINST_ARMOR = 0.01
    AGAINST_HULL = 1.75

    SHIELD_PIERCING = 0.05  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.10  # Percentage of initial damage that goes through to hull

    def __init__(self, scene: Scene, pos: Vector2, velocity: Vector2, scale=1):
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
    ACCURACY = 0.75

    CLIP_SIZE = 5
    RELOAD_TIME = 1500
    SHOOT_DELAY = 700
    MAX_AMMO = 25

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = ShotgunShot

    def _perform_shot(self, scene, pos, velocity):
        super()._perform_shot(scene, pos, velocity)
        audio.sound(f"assets/audio/gatling/shot{random.randint(1,3):02}.wav").play()
