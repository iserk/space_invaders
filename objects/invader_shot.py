import random

import pygame

from utils import audio
from utils.sprites import get_frames
from objects.position import Position
from objects.game_object import Sprite
from weapons.shot import Shot
from scenes.scene import Scene


class InvaderShot(Shot):
    SCORE = 50

    def __init__(self, scene: Scene, pos: Position, velocity: Position, scale=1):
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
            self.frame = 2
