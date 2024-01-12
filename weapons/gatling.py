import random

import pygame
from pygame import Vector2

from utils import audio
from utils.sprites import get_frames

from objects.game_object import Sprite

from weapons.hero_shot import HeroWeapon, HeroShot

from scenes.scene import Scene


class GatlingShot(HeroShot):
    SCORE_COST = 1
    DAMAGE = 8
    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.1
    AGAINST_ARMOR = 0.5
    AGAINST_HULL = 1.5

    SHIELD_PIERCING = 0.05  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.10  # Percentage of initial damage that goes through to hull

    def __init__(self, scene: Scene, pos: Vector2, velocity: Vector2, scale=1.25):
        # velocity += Position((np.random.default_rng().normal() - 0.5) * self.SPEED * (1 - self.ACCURACY), 0)

        super().__init__(scene, pos, velocity)
        self.roll = velocity.x / velocity.y

        self.scale = scale
        image = pygame.image.load("assets/images/gatling_shot.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 3),
            width=32 * scale,
            height=32 * scale,
        )


class Gatling(HeroWeapon):
    SPEED = 3000
    SHOOT_DELAY = 20
    PELLETS = 1
    ACCURACY = 0.95

    CLIP_SIZE = 100
    RELOAD_TIME = 1500
    MAX_AMMO = 600

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = GatlingShot

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        audio.sound(f"assets/audio/gatling/shot{random.randint(1,4):02}.wav").play()
