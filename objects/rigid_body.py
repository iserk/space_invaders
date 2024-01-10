import random

import pygame
from pygame import Vector2

from objects.game_object import GameObject
from objects.position import Position
from objects.game_object import Sprite
from objects.explosion import Explosion

from scenes.scene import Scene
from utils import collision, audio


class RigidBody(GameObject):
    MAX_HIT_POINTS = 1
    MAX_ARMOR = 0

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)

        self.hit_points = self.MAX_HIT_POINTS
        self.armor = self.MAX_ARMOR

        self.pos = pos.copy()
        self.prev_pos = pos.copy()

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
        self.prev_pos = self.pos.copy()

        super().update(dt)

        self.pos += self.velocity * dt / 1000
        self.roll += self.roll_speed * dt / 1000

        self.detect_collisions()

    def get_rect(self):
        return [
            Vector2(self.pos.x - self.sprite.width / 2, self.pos.y - self.sprite.height / 2),
            Vector2(self.pos.x + self.sprite.width / 2, self.pos.y + self.sprite.height / 2),
        ]

    def get_collider(self):
        return [
            Vector2(self.pos.x - self.sprite.width / 2, self.pos.y - self.sprite.height / 2),
            Vector2(self.pos.x + self.sprite.width / 2, self.pos.y - self.sprite.height / 2),
            Vector2(self.pos.x + self.sprite.width / 2, self.pos.y + self.sprite.height / 2),
            Vector2(self.pos.x - self.sprite.width / 2, self.pos.y + self.sprite.height / 2),
        ]

    def hit(self, damage=1, by=None):
        self.hit_points -= max(0, damage - self.armor)
        self.armor -= random.randint(0, round(damage / 2) + 1)

        if self.hit_points <= 0:
            self.is_active = False
            self.will_destroy(by=by)

        # else:
        #     audio.sound(f"assets/audio/shield_hit{random.randint(1, 2)}.wav", volume=0.5).play()

        audio.sound(f"assets/audio/shot_hit{random.randint(1, 2)}.mp3", volume=0.2).play()

    def on_collision(self, obj=None):
        pass

    def detect_collisions(self):
        # This version detects collisions between the hero and other objects
        r = self.get_rect()
        sminx = min(r[0].x, r[1].x)
        smaxx = max(r[0].x, r[1].x)
        sminy = min(r[0].y, r[1].y)
        smaxy = max(r[0].y, r[1].y)

        for obj in self.scene.objects:
            if obj != self and isinstance(obj, RigidBody):
                r = obj.get_rect()
                ominx = min(r[0].x, r[1].x)
                omaxx = max(r[0].x, r[1].x)
                ominy = min(r[0].y, r[1].y)
                omaxy = max(r[0].y, r[1].y)

                # if (obj.pos.x - obj.sprite.width / 2 < self.pos.x < obj.pos.x + obj.sprite.width / 2
                #         and obj.pos.y - obj.sprite.height / 2 < self.pos.y < obj.pos.y + obj.sprite.height / 2):

                # Detect if two rectangles overlap
                if (sminx <= omaxx and smaxx >= ominx
                        and sminy <= omaxy and smaxy >= ominy):

                # if collision.sat_collision_check(self.get_collider(), obj.get_collider()):

                    # print(f'Collision between {self} and {obj}')
                    self.on_collision(obj)
                    obj.on_collision(obj)
                pass

    def will_destroy(self, by=None):
        self.destroy()
