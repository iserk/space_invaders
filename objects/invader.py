import random
import math

import pygame

from utils.noise import fractal_noise
from objects.invader_shot import InvaderShot

from objects.position import Position
from objects.game_object import Sprite
from objects.vehicle import Vehicle
from objects.explosion import Explosion
from scenes.scene import Scene
from game.game_manager import GameStatus, SceneSwitchException


class Invader(Vehicle):
    SPEED = 20
    # SPEED = 0
    ANIMATION_FPS = 2
    SCORE = 100
    MAX_HIT_POINTS = 4

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene, pos, sprite)

        self.hit_points = self.MAX_HIT_POINTS
        self.initial_pos = pos.copy()
        self.velocity = Position(0, Invader.SPEED)

    def draw(self, camera):
        super().draw(camera)

        # # Draw rectangle around the invader
        #
        # pygame.draw.rect(
        #     camera.screen,
        #     (255, 0, 0),
        #     (
        #         self.pos.x - self.sprite.width / 2,
        #         self.pos.y - self.sprite.height / 2,
        #         self.sprite.width,
        #         self.sprite.height,
        #     ),
        #     1
        # )

        # Draw a green bar above the invader to indicate its health
        if self.MAX_HIT_POINTS > 10:
            pygame.draw.rect(
                camera.screen,
                (0, 255, 0),
                (
                    self.pos.x - self.sprite.width / 2,
                    self.pos.y - self.sprite.height / 2 - 10,
                    self.sprite.width * self.hit_points / self.MAX_HIT_POINTS,
                    2,
                )
            )
        elif self.MAX_HIT_POINTS > 1:
            for i in range(self.hit_points):
                pygame.draw.rect(
                    camera.screen,
                    (0, 255, 0),
                    (
                        self.pos.x - self.sprite.width / 2 + i * self.sprite.width / self.MAX_HIT_POINTS + 2,
                        self.pos.y - self.sprite.height / 2 - 10,
                        self.sprite.width / self.MAX_HIT_POINTS - 2,
                        2,
                    )
                )

        # # Draw a blue circle around the invader to indicate its health (as shields)
        # for i in range(self.hit_points - 1):
        #     pygame.draw.circle(
        #         camera.screen,
        #         (64, 80, 255),
        #         (round(self.pos.x), round(self.pos.y)),
        #         self.sprite.width / 2 + 8 + 4 * i,
        #         2
        #     )

    def update(self, dt):
        super().update(dt)

        self.frame = round(Invader.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)

        if self.is_active:
            # self.pos.x = self.initial_pos.x + round(math.sin(self.pos.y / 8) * 40)
            self.velocity.x = round(math.sin(self.pos.y / 8) * 40)

        if (self.pos.y > self.scene.game.screen_size[1] - self.sprite.height
                and self.scene.game.status == GameStatus.PLAYING):

            raise SceneSwitchException(self.scene.game.scenes[1])
            # self.scene.game.switch_to_scene(self.scene.game.scenes[1])
            # return

        if self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()

        if (self.is_active
                and fractal_noise(self.scene.total_time / 1000 + self.pos.x + self.pos.y, 5, 1) > 0.5
                and self.scene.total_time % 1000 < 20):
            InvaderShot(
                scene=self.scene,
                pos=self.pos + Position(0, self.sprite.height / 2),
                velocity=Position(0, InvaderShot.SPEED),
            )
            # pass

    def explode(self):
        Explosion(scene=self.scene, pos=self.pos, scale=random.randint(2, 8))
