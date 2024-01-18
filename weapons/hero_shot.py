import random

import numpy as np
import pygame

from pygame import Vector2

from utils import audio
from weapons.weapon import Weapon

from weapons.invader_shot import InvaderShot
from weapons.shot import Shot, ShotState
from objects.invader import Invader
from scenes.scene import Scene


class HeroShot(Shot):
    """Base class for hero shots"""

    SCORE_COST = 1
    DAMAGE = 100
    CRITICAL_HIT_CHANCE = 0.2
    VALID_TARGETS_CLASSES = [Invader, InvaderShot]

    def __init__(self, scene: Scene, pos: Vector2, velocity: Vector2):

        super().__init__(scene, pos, velocity)

        # self.scene.game.traumatize(0.1)
        self.scene.game.score -= round(self.SCORE_COST)

    def on_collision(self, obj=None):
        if not obj.is_active or not any([isinstance(obj, cls) for cls in self.VALID_TARGETS_CLASSES]):
            return

        damage = self.get_damage()
        # self.scene.game.traumatize(0.1 * damage)
        if np.random.default_rng().random() <= self.CRITICAL_HIT_CHANCE:
            damage *= 2
            print(f"{self}: damage for {damage}; critical hit!")
        else:
            print(f"{self}: damage for {damage}")

        if random.random() <= self.RICOCHET_CHANCE:
            print(f"{self}: ricochet!")
            # normal = Vector2(0, 1)
            # normal = normal.rotate(random.randint(-45, 45))
            # self.velocity = self.velocity.reflect(normal)
            angle = random.randint(-45, 45)
            self.velocity = self.velocity.rotate(-angle)
            self.roll = angle
            self.roll_speed = random.randint(-100, 100)

            ricochet_damage = damage * self.RICOCHET_DAMAGE_PERCENTAGE
            damage -= ricochet_damage

            # Play ricochet sound
            audio.sound(f"assets/audio/ricochet/{random.randint(1,7):02}.mp3").play()
        else:
            audio.sound(f"assets/audio/shot_hit{random.randint(1, 2)}.mp3", volume=0.7).play()
            print("hit!")
            ricochet_damage = 0

        # audio.sound(f"assets/audio/ricochet/{random.randint(1,7):02}.mp3", volume=0.5).play()

        excess_damage = obj.hit(damage=damage, by=self)
        print(f"{self}: damage: {damage}, ricochet damage: {ricochet_damage}, excess damage: {excess_damage}")
        remaining_damage = max(0, excess_damage) + ricochet_damage

        if obj.hit_points <= 0:
            self.scene.game.score += round(obj.SCORE)

        if not self.DESTROY_ON_HIT and remaining_damage > 0:
            speed = self.damage2speed(remaining_damage)
            if speed < self.SPEED * 0.1:
                self.state = ShotState.DESTROYED
            else:
                self.velocity = self.velocity.normalize() * speed
                self.state = ShotState.HITTING
        else:
            self.state = ShotState.DESTROYED

        self.frame = self.state2frame()

class HeroWeapon(Weapon):
    """Base class for hero weapons"""
    pass
