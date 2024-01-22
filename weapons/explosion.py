import math
import random

import pygame
from pygame import Vector2

import utils.time
from objects.explosion_effect import ExplosionEffect
from objects.rigid_body import RigidBody
from weapons.hero_shot import HeroShot

from scenes.scene import Scene
from weapons.shot import ShotState


class Explosion(HeroShot):
    WINDAGE = 0.25
    MASS = 0.01
    SPEED = 300
    DAMAGE = 5000
    DESTROY_ON_HIT = False

    CRITICAL_HIT_CHANCE = 0.1

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 0.001
    AGAINST_ARMOR = 0.01
    AGAINST_HULL = 1.25

    SHIELD_PIERCING = 0.05  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.10  # Percentage of initial damage that goes through to hull

    SHOT_SIZE = (500, 500)

    VALID_TARGETS_CLASSES = [RigidBody]

    def __init__(self, scene: Scene, pos: Vector2, damage=DAMAGE, scale=None):
        super().__init__(scene, pos, velocity=Vector2(0, 0))
        self.damage = damage
        if scale is None:
            scale = max(2.0, math.log(damage, 10))

        self.start_time = self.scene.game.total_time

        self.affected_targets = []

        self.explosion_effects = [
            ExplosionEffect(
                scene=self.scene,
                pos=self.pos + Vector2(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                ) * 5 * i,
                scale=i
            ) for i in range(1, random.randint(3, 16), random.randint(2, 4))
        ]

        # print(f">>> {self} created with pos={self.pos}, damage={self.damage}")

    def on_collision(self, obj=None):
        # print(f"[><] {self.scene.game.total_time} {self}: Colliding with {obj}")
        if not obj.is_active or not any([isinstance(obj, cls) for cls in self.VALID_TARGETS_CLASSES]):
            return

        self.affected_targets.append(obj)
        self.state = ShotState.HITTING

    def update(self, dt):
        if self.state == ShotState.STARTING:
            self.state = ShotState.FLYING

        super().update(dt)

        if self.scene.game.total_time - self.start_time > 2 * utils.time.TIME_UNITS_PER_SECOND:
            self.destroy()

        # print(f"[+] Affected targets: ({len(self.affected_targets)}) {self.affected_targets}")

        if self.state == ShotState.HITTING:
            for obj in self.affected_targets:
                if not obj.is_active:
                    continue

                # Distance between self.pos and obj.pos
                distance = (self.pos - obj.pos).length()
                # print("Distance", distance)

                # Calculate damage based on critical hit chance
                damage = min(self.damage, self.damage * 10 / (distance ** 2)) if distance > 0 else self.damage
                self.scene.game.traumatize(0.1 * damage)

                if random.random() <= self.CRITICAL_HIT_CHANCE:
                    damage *= 2

                # print(f"{self}: damage {obj} for {damage}")
                obj.hit(damage=damage, by=self)

                if obj.hit_points <= 0 and hasattr(obj, "SCORE"):
                    self.scene.game.score += obj.SCORE

        self.affected_targets = []

    def get_rect(self):
        return [
            Vector2(self.pos.x - self.SHOT_SIZE[0] / 2, self.pos.y - self.SHOT_SIZE[1] / 2),
            Vector2(self.pos.x + self.SHOT_SIZE[0] / 2, self.pos.y + self.SHOT_SIZE[1] / 2),
        ]

    def draw(self, camera):
        for effect in self.explosion_effects:
            effect.draw(camera)

        # # Draw rectangle from get_rect()
        # r = self.get_rect()
        # pygame.draw.rect(
        #     camera.screen,
        #     (0, 255, 255),
        #     # self.get_rect(),
        #     (
        #         r[0].x,
        #         r[0].y,
        #         r[1].x - r[0].x,
        #         r[1].y - r[0].y,
        #     ),
        #     10
        # )


