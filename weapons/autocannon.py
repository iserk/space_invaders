import random

import pygame
from pygame import Vector2

from utils import audio
from utils.sprites import get_frames

from objects.game_object import Sprite

from weapons.hero_shot import HeroWeapon, HeroShot

from scenes.scene import Scene


class AutocannonShot(HeroShot):
    WINDAGE = 0.025
    MASS = 1
    SPEED = 3000
    DAMAGE = 32
    SCORE_COST = DAMAGE
    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.002
    AGAINST_ARMOR = 0.02
    AGAINST_HULL = 1.25

    SHIELD_PIERCING = 0.10  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.15  # Percentage of initial damage that goes through to hull

    def __init__(self, scene: Scene, pos: Vector2, velocity: Vector2, scale=2):
        # velocity += Position((np.random.default_rng().normal() - 0.5) * self.SPEED * (1 - self.ACCURACY), 0)

        super().__init__(scene, pos, velocity)

        self.scale = scale
        image = pygame.image.load("assets/images/gatling_shot.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 3),
            width=32 * scale,
            height=32 * scale,
        )


class Autocannon(HeroWeapon):
    SHOOT_DELAY = 150
    ACCURACY = 0.96

    CLIP_SIZE = 25
    RELOAD_TIME = 1500
    MAX_AMMO = 100

    RECOIL_FACTOR = 5

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = AutocannonShot

    def _perform_shot(self, scene, pos, velocity):
        super()._perform_shot(scene, pos, velocity)
        audio.sound(f"assets/audio/gatling/shot{random.randint(1,4):02}.wav").play()
