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


class CannonShot(HeroShot):
    SCORE_COST = 2
    DAMAGE = 24

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

        # self.scene.game.traumatize(0.1)

        self.frame = 0
        self.scene.game.score -= self.SCORE_COST

    def on_collision(self, obj=None):
        if self.damage <= 0:
            self.frame = 2
            return

        if isinstance(obj, Invader) or isinstance(obj, InvaderShot) and obj.is_active and obj.hit_points > 0:
            self.scene.game.traumatize(0.2)

            remaining_damage = self.damage - max(0, obj.hit_points)

            # print(f"DMG: {self.damage}, HP: {obj.hit_points}, RD: {remaining_damage}")
            obj.hit(damage=self.damage, by=self)
            if obj.hit_points <= 0:
                self.scene.game.score += obj.SCORE

            self.damage = remaining_damage
            # print(self.damage)
            if self.damage <= 0:
                self.frame = 2


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
