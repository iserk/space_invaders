import random
import numpy as np

import pygame

from utils import audio
from weapons.weapon import Weapon

from objects.invader_shot import InvaderShot
from weapons.shot import Shot, ShotState
from objects.invader import Invader
from objects.position import Position
from objects.game_object import Sprite
from scenes.scene import Scene

from utils.sprites import get_frames


class HeroShot(Shot):
    """Base class for hero shots"""

    SCORE_COST = 1
    DAMAGE = 100
    CRITICAL_HIT_CHANCE = 0.2
    VALID_TARGETS_CLASSES = [Invader, InvaderShot]

    def __init__(self, scene: Scene, pos: Position, velocity: Position):

        super().__init__(scene, pos, velocity)

        # self.scene.game.traumatize(0.1)
        self.scene.game.score -= self.SCORE_COST

    def on_collision(self, obj=None):
        if not obj.is_active or not any([isinstance(obj, cls) for cls in self.VALID_TARGETS_CLASSES]):
            return

        # Calculate damage based on critical hit chance
        damage = self.DAMAGE
        # self.scene.game.traumatize(0.1 * damage)

        if np.random.default_rng().random() <= self.CRITICAL_HIT_CHANCE:
            damage *= 2
            print(self, ": critical hit!")

        remaining_damage = max(0, obj.hit(damage=self.damage, by=self))

        if obj.hit_points <= 0:
            self.scene.game.score += obj.SCORE

        # print(f"DMG: {self.damage}, HP: {obj.hit_points}, RD: {remaining_damage}")

        self.damage = remaining_damage

        if not self.DESTROY_ON_HIT and self.damage > 0:
            self.state = ShotState.HITTING
        else:
            self.state = ShotState.DESTROYED

        self.frame = self.state2frame()



class HeroWeapon(Weapon):
    """Base class for hero weapons"""
    pass
