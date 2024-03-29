import random

import pygame
from pygame import Vector2

import settings
from objects.game_object import GameObject

from objects.game_object import Sprite

from scenes.scene import Scene
from utils import audio


class RigidBody(GameObject):
    MAX_HIT_POINTS = 1
    MAX_ARMOR = 0
    MAX_SHIELD = 0
    WINDAGE = 0.5
    MASS = 1

    def __init__(self, scene: Scene, pos: Vector2, sprite: Sprite):
        super().__init__(scene)

        self.hit_points = self.MAX_HIT_POINTS
        self.armor = self.MAX_ARMOR
        self.shield = self.MAX_SHIELD

        self.pos = pos.copy()
        self.prev_pos = pos.copy()

        self.velocity = Vector2(0, 0)

        self.roll = 0  # Roll angle in degrees
        self.roll_speed = 0  # Roll speed in degrees per second

        self.sprite = sprite
        self.frame = 0

        self.is_taking_damage = False
        self.is_active = True

    def draw(self, camera):
        image = self.sprite.frames[self.frame]
        if self.roll != 0:
            image = pygame.transform.rotate(image, self.roll)
        if self.is_taking_damage:
            image = image.copy()
            # image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_ADD)
            image.fill((255, 128, 128, 200), None, pygame.BLEND_RGBA_MULT)
        camera.screen.blit(
            image,
            tuple(self.pos - Vector2(self.sprite.width / 2, self.sprite.height / 2))
        )

    def get_acceleration(self):
        return -self.velocity * self.WINDAGE / self.MASS if self.WINDAGE != 0 else Vector2(0, 0)

    def update(self, dt):
        self.is_taking_damage = False

        self.prev_pos = self.pos.copy()

        super().update(dt)
        self.velocity += self.get_acceleration() * dt / settings.TIME_UNITS_PER_SECOND

        self.pos += self.velocity * dt / settings.TIME_UNITS_PER_SECOND
        self.roll += self.roll_speed * dt / settings.TIME_UNITS_PER_SECOND

        self.detect_collisions()

    def get_rect(self):
        return [
            Vector2(self.pos.x - self.sprite.width / 2, self.pos.y - self.sprite.height / 2),
            Vector2(self.pos.x + self.sprite.width / 2, self.pos.y + self.sprite.height / 2),
        ]

    def hit(self, damage=1, by=None) -> int:
        """
        Processes a hit by a weapon.
        Returns the amount of damage that was not absorbed by the shields, armor and hull.
        :param damage: Damage from the weapon
        :param by: Projectile that hit this object
        :return: Damage that was not absorbed
        """
        from weapons.shot import Shot

        self.is_taking_damage = True

        if not self.is_active:
            return damage

        if isinstance(by, Shot):
            against_shields = by.AGAINST_SHIELD
            against_armor = by.AGAINST_ARMOR
            against_hull = by.AGAINST_HULL
            shield_piercing = by.SHIELD_PIERCING
            armor_piercing = by.ARMOR_PIERCING
        else:
            against_shields = 0.5
            against_armor = 0.5
            against_hull = 1
            shield_piercing = armor_piercing = 0

        shield_damage = damage * against_shields
        damage_after_shield = damage - self.shield * (1 - shield_piercing)
        armor_damage = damage_after_shield * against_armor

        damage_after_armor = damage_after_shield - self.armor * (1 - armor_piercing)
        hull_damage = damage_after_armor * against_hull

        excess_damage = max(0, damage_after_armor - max(0, self.hit_points))
        # print(f'{self} hit by {by} for {damage} damage (shield: {shield_damage}, armor: {armor_damage}, hull: {hull_damage}), excess: {excess_damage}')

        self.hit_points -= max(0, hull_damage)
        self.armor -= max(0, armor_damage)
        self.shield -= max(0, shield_damage)

        if self.hit_points <= 0:
            self.is_active = False
            self.will_destroy(by=by)

        # else:
        #     audio.sound(f"assets/audio/shield_hit{random.randint(1, 2)}.wav", volume=0.5).play()

        # audio.sound(f"assets/audio/shot_hit{random.randint(1, 2)}.mp3", volume=0.2).play()

        return excess_damage

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
                    obj.on_collision(self)
                pass

    def will_destroy(self, by=None):
        self.destroy()
