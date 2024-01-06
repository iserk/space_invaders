import random
import math

import pygame

from objects.position import Position
from objects.game_object import Sprite
from objects.vehicle import Vehicle
from objects.explosion import Explosion
from scenes.scene import Scene
from game.game_manager import GameStatus, SceneSwitchException


class Invader(Vehicle):
    # SPEED = 20
    SPEED = 0
    ANIMATION_FPS = 2
    SCORE = 100

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene, pos, sprite)

        self.initial_pos = pos.copy()
        self.velocity = Position(0, Invader.SPEED)

    def draw(self, camera):
        pygame.draw.circle(camera.screen, (255, 0, 0), tuple(self.initial_pos), 5)
        camera.screen.blit(
            self.sprite.frames[round(Invader.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos - Position(self.sprite.width / 2, self.sprite.height / 2))
        )

    def update(self, dt):
        if not self.is_active:
            print("Inactive invader")

        self.pos += self.velocity * dt / 1000

        if self.is_active:
            self.pos.x = self.initial_pos.x + round(math.sin(self.pos.y / 8) * 40)

        if (self.pos.y > self.scene.game.screen_size[1] - self.sprite.height
                and self.scene.game.status == GameStatus.PLAYING):

            raise SceneSwitchException(self.scene.game.scenes[1])
            # self.scene.game.switch_to_scene(self.scene.game.scenes[1])
            # return

        if self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()

        # if fractal_noise(self.scene.total_time / 1000 + self.pos.x + self.pos.y, 5, 1) > 0.5 and self.scene.game.total_time % 1000 < 10:
        #     InvaderShot(
        #         scene=self.scene,
        #         pos=self.pos + Position(self.sprite.width / 2, self.sprite.height),
        #         velocity=Position(0, InvaderShot.SPEED),
        #     )

    def destroy(self, explode=False):
        super().destroy(explode=False)
        self.scene.game.score += Invader.SCORE
        if explode:
            Explosion(scene=self.scene, pos=self.pos, scale=random.randint(2, 8))

