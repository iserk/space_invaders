import random

import pygame
from pygame import Vector2

from utils import audio
from utils.sprites import get_frames
from objects.game_object import Sprite
from weapons.shot import Shot, ShotState
from scenes.scene import Scene


class InvaderShot(Shot):
    SCORE = 50
    DAMAGE = 64
    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.25
    AGAINST_ARMOR = 0.5
    AGAINST_HULL = 0.5

    SHIELD_PIERCING = 0.0  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.0  # Percentage of initial damage that goes through to hull

    def __init__(self, scene: Scene, pos: Vector2, velocity: Vector2, scale=1):
        super().__init__(scene, pos, velocity)
        audio.sound(f"assets/audio/invader_shot{random.randint(1, 2)}.wav", volume=0.4).play()

        self.scale = scale
        image = pygame.image.load("assets/images/invader_shot.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 3),
            width=32 * scale,
            height=32 * scale,
        )

    def update(self, dt):
        super().update(dt)

        if self.frame == 2:
            self.destroy()
            return

    def on_collision(self, obj=None):
        # Importing here to avoid circular imports
        from objects.hero import Hero

        # self.scene.game.traumatize(0.05)
        if isinstance(obj, Hero):
            obj.hit(damage=self.DAMAGE, by=self)
            self.state = ShotState.DESTROYED
            self.frame = self.state2frame()
