import random

import pygame

from objects.game_object import GameObject
from objects.position import Position
from objects.game_object import Sprite
from objects.explosion import Explosion

from scenes.scene import Scene


class RigidBody(GameObject):
    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)

        self.hit_points = 1

        self.pos = pos
        self.velocity = Position(0, 0)

        self.roll = 0  # Roll angle in degrees
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

        self.detect_collisions()

    def hit(self, damage=1, obj=None):
        self.hit_points -= damage

        velocity_y_sign = 1 if obj.velocity.y >= 0 else -1

        torque = (self.pos.x - obj.pos.x) / self.sprite.width / 2 * velocity_y_sign
        self.pos.y += (1 - torque) * velocity_y_sign * 10

        if self.hit_points <= 0:
            self.will_destroy(obj, torque)

        # else:
        #     sound = pygame.mixer.Sound(f"assets/audio/shield_hit{random.randint(1, 2)}.wav")
        #     sound.set_volume(0.5)
        #     sound.play()

        sound = pygame.mixer.Sound(f"assets/audio/shot_hit{random.randint(1, 2)}.mp3")
        sound.set_volume(0.2)
        sound.play()

    def collide(self, obj=None):
        pass

    def detect_collisions(self):
        for obj in self.scene.objects:
            if (obj != self
                    and obj.pos.x - obj.sprite.width / 2 <= self.pos.x <= obj.pos.x + obj.sprite.width / 2
                    and obj.pos.y - obj.sprite.height / 2 <= self.pos.y <= obj.pos.y + obj.sprite.height / 2):
                self.collide(obj)

    def will_destroy(self, other_obj=None, torque=0):
        self.destroy()