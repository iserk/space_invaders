import random

import pygame

from objects.position import Position

from objects.shot import Shot
from objects.explosion import Explosion
from scenes.scene import Scene


class InvaderShot(Shot):
    COLOR = (255, 63, 63)

    def __init__(self, scene: Scene, pos: Position, velocity: Position):
        super().__init__(scene, pos, velocity, InvaderShot.COLOR)
        pygame.mixer.Sound(f"assets/audio/invader_shot{random.randint(1, 2)}.wav").play()

    def update(self, dt):
        super().update(dt)

        if hasattr(self.scene, "hero"):
            hero = self.scene.hero
            if (hero.pos.x - hero.sprite.width / 2 <= self.pos.x <= hero.pos.x + hero.sprite.width / 2
                    and hero.pos.y - hero.sprite.width / 2 <= self.pos.y <= hero.pos.y + hero.sprite.height / 2):
                Explosion(scene=self.scene, pos=hero.pos, scale=8)
                hero.destroy()
                self.destroy()

