import random

import pygame
from pygame import Vector2

from utils import audio
from utils.sprites import get_frames

from objects.game_object import Sprite

from weapons.hero_shot import HeroWeapon, HeroShot

from scenes.scene import Scene


class CannonShot(HeroShot):
    DAMAGE = 400
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

    def __init__(self, scene: Scene, pos: Vector2, velocity: Vector2, scale=2):
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
    ACCURACY = 0.97

    CLIP_SIZE = 1
    RELOAD_TIME = 1200
    MAX_AMMO = 20

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = CannonShot

    def _perform_shot(self, scene, pos, velocity):
        super()._perform_shot(scene, pos, velocity)
        audio.sound(f"assets/audio/cannon/shot{random.randint(1, 2):02}.wav", volume=3).play()
