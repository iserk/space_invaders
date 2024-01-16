import math
import random

import numpy as np
import pygame
from pygame import Vector2

import settings
from objects.explosion import Explosion
from utils import audio
from utils.sprites import get_frames

from objects.game_object import Sprite

from weapons.hero_shot import HeroWeapon, HeroShot

from scenes.scene import Scene
from weapons.shot import ShotState


class Missile(HeroShot):
    SPEED = 150  # Initial speed
    ACCELERATION = 2  # Pixels per second squared

    DAMAGE = 1000
    SCORE_COST = DAMAGE
    DESTROY_ON_HIT = False

    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.1
    AGAINST_ARMOR = 1.25
    AGAINST_HULL = 0.75

    SHIELD_PIERCING = 0.25  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.25  # Percentage of initial damage that goes through to hull

    # SHOT_SIZE = (256, 128)

    def __init__(self, scene: Scene, pos: Vector2, velocity: Vector2, scale=2):
        # velocity += Position((np.random.default_rng().normal() - 0.5) * self.SPEED * (1 - self.ACCURACY), 0)

        super().__init__(scene, pos, velocity)
        self.roll = math.atan(velocity.x / velocity.y) / (2 * math.pi) * 360

        self.scale = scale
        image = pygame.image.load("assets/images/missile.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 6),
            width=32 * scale,
            height=32 * scale,
        )

    def on_collision(self, obj=None):
        if not obj.is_active or not any([isinstance(obj, cls) for cls in self.VALID_TARGETS_CLASSES]):
            return

        # Calculate damage based on critical hit chance
        damage = self.DAMAGE
        # self.scene.game.traumatize(0.1 * damage)

        if np.random.default_rng().random() <= self.CRITICAL_HIT_CHANCE:
            damage *= 2
            print(f"{self}: critical hit!")

        remaining_damage = max(0, obj.hit(damage=self.damage, by=self))

        if obj.hit_points <= 0:
            self.scene.game.score += round(obj.SCORE)

        for i in range(2, random.randint(3, 16), random.randint(2, 4)):
            Explosion(
                scene=self.scene,
                pos=self.pos + Vector2(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                ) * 2 * i,
                scale=i
            )

        # Explosion(scene=self.scene, pos=self.pos, scale=12)
        # Explosion(scene=self.scene, pos=self.pos, scale=9)
        # Explosion(scene=self.scene, pos=self.pos, scale=4)
        # Explosion(scene=self.scene, pos=self.pos, scale=2)

        self.state = ShotState.DESTROYED

        self.frame = self.state2frame()

    def state2frame(self):
        match self.state:
            case ShotState.STARTING:
                return 0
            case ShotState.FLYING:
                return 1 + round(self.scene.game.total_time / 60) % 4
            case ShotState.HITTING:
                return 5
            case ShotState.DESTROYED:
                return 5

    def update(self, dt):
        super().update(dt)
        self.frame = self.state2frame()
        self.velocity *= (1 + dt * self.ACCELERATION / settings.TIME_UNITS_PER_SECOND)


class MissileLauncher(HeroWeapon):
    SHOOT_DELAY = 800
    PELLETS = 1
    ACCURACY = 0.95

    CLIP_SIZE = 1
    RELOAD_TIME = 1500
    MAX_AMMO = 10

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = Missile

    def _perform_shot(self, scene, pos, velocity):
        super()._perform_shot(scene, pos, velocity)
        audio.sound(f"assets/audio/missile/shot{random.randint(1, 3):02}.wav", volume=3).play()
