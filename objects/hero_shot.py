import random
import numpy as np

import pygame

from objects.shot import Shot
from objects.invader import Invader
from objects.position import Position
from objects.game_object import Sprite
from scenes.scene import Scene

from utils.sprites import get_frames


class HeroShot(Shot):
    SCORE_COST = 10
    SPEED = 500
    COLOR = (0, 255, 255)
    DAMAGE = 1

    def __init__(self, scene: Scene, pos: Position, velocity: Position, scale=2):
        velocity += Position((np.random.default_rng().normal() - 0.5 ) * self.SPEED / 10, 0)

        super().__init__(scene, pos, velocity, HeroShot.COLOR)

        self.scene.game.traumatize(0.1)

        self.scale = scale
        image = pygame.image.load("assets/images/hero_shot.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 3),
            width=32 * scale,
            height=32 * scale,
        )

        self.frame = 0
        self.scene.game.score -= HeroShot.SCORE_COST
        pygame.mixer.Sound("assets/audio/hero_shot.wav").play()

    def update(self, dt):
        super().update(dt)

        if self.frame == 2:
            self.destroy()
            return

        for enemy in self.scene.objects:
            if (isinstance(enemy, Invader)
                    and enemy.pos.x - enemy.sprite.width / 2 <= self.pos.x <= enemy.pos.x + enemy.sprite.width / 2
                    and enemy.pos.y - enemy.sprite.height / 2 <= self.pos.y <= enemy.pos.y + enemy.sprite.height / 2):

                enemy.hit(damage=self.DAMAGE, obj=self)
                if enemy.hit_points <= 0:
                    self.scene.game.score += Invader.SCORE
                self.frame = 2

    def draw(self, camera):
        camera.screen.blit(
            self.sprite.frames[self.frame],
            tuple(self.pos - Position(self.sprite.width / 2, self.sprite.height / 2))
        )
        if self.frame == 0:
            self.frame = 1

