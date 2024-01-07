import random

import pygame

from objects.position import Position
from objects.game_object import Sprite
from objects.shot import Shot
from objects.explosion import Explosion
from scenes.scene import Scene
from utils.sprites import get_frames


class InvaderShot(Shot):

    def __init__(self, scene: Scene, pos: Position, velocity: Position, scale=1):
        super().__init__(scene, pos, velocity)
        pygame.mixer.Sound(f"assets/audio/invader_shot{random.randint(1, 2)}.wav").play()

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

        if hasattr(self.scene, "hero"):
            hero = self.scene.hero
            if (hero.pos.x - hero.sprite.width / 2 <= self.pos.x <= hero.pos.x + hero.sprite.width / 2
                    and hero.pos.y - hero.sprite.width / 2 <= self.pos.y <= hero.pos.y + hero.sprite.height / 2):

                hero.hit(damage=self.DAMAGE, obj=self)
                self.frame = 2
