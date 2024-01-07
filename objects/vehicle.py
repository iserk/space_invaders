import random

import pygame

from objects.game_object import GameObject
from objects.position import Position
from objects.game_object import Sprite
from objects.explosion import Explosion

from scenes.scene import Scene


class Vehicle(GameObject):
    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)

        self.hit_points = 1

        self.pos = pos
        self.velocity = Position(0, 0)

        self.roll = 0   # Roll angle in degrees
        self.roll_speed = 0  # Roll speed in degrees per second

        self.sprite = sprite
        self.frame = 0

        self.is_active = True

    def draw(self, camera):
        image = self.sprite.frames[self.frame]
        if self.roll != 0:
            image = pygame.transform.rotate(image, self.roll)
        camera.screen.blit(
            image,
            tuple(self.pos - Position(self.sprite.width / 2, self.sprite.height / 2))
        )

    def update(self, dt):
        super().update(dt)

        self.pos += self.velocity * dt / 1000
        self.roll += self.roll_speed * dt / 1000

    def hit(self, damage=1, obj=None):
        self.hit_points -= damage

        torque = (obj.pos.x - self.pos.x) / self.sprite.width / 2
        self.pos.y -= 10 * (1 - torque)

        if self.hit_points <= 0:
            self.scene.add_timer(random.randint(20, 300), lambda o=self: o.destroy(explode=True))
            self.roll = torque * 60
            self.roll_speed = torque * 360
            self.velocity = obj.velocity.get_normalized() * 10

        # else:
        #     sound = pygame.mixer.Sound(f"assets/audio/shield_hit{random.randint(1, 2)}.wav")
        #     sound.set_volume(0.5)
        #     sound.play()

        sound = pygame.mixer.Sound(f"assets/audio/shot_hit{random.randint(1, 2)}.mp3")
        sound.set_volume(0.2)
        sound.play()


    def destroy(self, explode=False):
        super().destroy()
        if explode:
            Explosion(scene=self.scene, pos=self.pos, scale=8)

