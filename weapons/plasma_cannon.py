import random

import pygame

from utils import audio
from utils.sprites import get_frames

from objects.position import Position
from objects.game_object import Sprite

from weapons.hero_shot import HeroWeapon, HeroShot

from scenes.scene import Scene


class PlasmaCannonShot(HeroShot):
    SCORE_COST = 2
    DAMAGE = 3
    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 1.5
    AGAINST_ARMOR = 0.25
    AGAINST_HULL = 0.5

    SHIELD_PIERCING = 0.0  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.00  # Percentage of initial damage that goes through to hull

    def __init__(self, scene: Scene, pos: Position, velocity: Position, scale=1):
        # velocity += Position((np.random.default_rng().normal() - 0.5) * self.SPEED * (1 - self.ACCURACY), 0)

        super().__init__(scene, pos, velocity)

        self.scale = scale
        image = pygame.image.load("assets/images/invader_shot.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 3),
            width=32 * scale,
            height=32 * scale,
        )

        # self.scene.game.traumatize(0.1)

        self.frame = 0
        self.scene.game.score -= self.SCORE_COST


class PlasmaCannon(HeroWeapon):
    SPEED = 3000
    SHOOT_DELAY = 150
    PELLETS = 1
    ACCURACY = 0.8

    CLIP_SIZE = 25
    RELOAD_TIME = 1500
    MAX_AMMO = 100

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = PlasmaCannonShot

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        print("__str__")
        return "Plasma Cannon"

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        audio.sound(f"assets/audio/gatling/shot{random.randint(1,4):02}.wav").play()
