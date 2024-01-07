import random

import pygame

from game.game_manager import SceneSwitchException
from objects.explosion import Explosion
from objects.position import Position
from objects.game_object import Sprite
from objects.vehicle import Vehicle
from objects.hero_shot import HeroShot
from scenes.scene import Scene


class Hero(Vehicle):
    SPEED = 300
    ANIMATION_FPS = 6
    SHOOT_DELAY = 200

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene, pos, sprite)
        self.prev_shot_time = 0

    def update(self, dt):
        super().update(dt)

        self.frame = round(Hero.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)

        if self.scene.is_input_enabled:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.pos.x -= self.SPEED * self.scene.game.dt / 1000
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.pos.x += self.SPEED * self.scene.game.dt / 1000
            if keys[pygame.K_SPACE]:
                if self.scene.game.total_time - self.prev_shot_time > self.SHOOT_DELAY:
                    self.prev_shot_time = self.scene.game.total_time
                    HeroShot(
                        scene=self.scene,
                        pos=self.pos + Position(0, -self.sprite.height / 2),
                        velocity=Position(0, -HeroShot.SPEED),
                    )

        # Hero will appear from another side of the screen if he goes out of bounds
        if self.pos.x < 0:
            self.pos.x = self.scene.game.screen_size[0] - self.sprite.width
        elif self.pos.x > self.scene.game.screen_size[0] - self.sprite.width:
            self.pos.x = 0

    def destroy(self, explode=False):
        super().destroy(explode)
        self.scene.game.traumatize(1)
        raise SceneSwitchException(self.scene.game.scenes[1])
        # self.scene.game.switch_to_scene(self.scene.game.scenes[1])

    def explode(self):
        Explosion(scene=self.scene, pos=self.pos, scale=12)
