import random
import numpy as np

import pygame

from utils import audio
from weapons.weapon import Weapon

from objects.invader_shot import InvaderShot
from weapons.shot import Shot
from objects.invader import Invader
from objects.position import Position
from objects.game_object import Sprite
from scenes.scene import Scene

from utils.sprites import get_frames


class HeroShot(Shot):
    """Base class for hero shots"""

    SCORE_COST = 1
    DAMAGE = 1
    CRITICAL_HIT_CHANCE = 0.2
    VALID_TARGETS_CLASSES = [Invader, InvaderShot]

    def __init__(self, scene: Scene, pos: Position, velocity: Position):

        super().__init__(scene, pos, velocity)

        # self.scene.game.traumatize(0.1)

        self.frame = 0
        self.scene.game.score -= self.SCORE_COST

    def on_collision(self, obj=None):
        if any([isinstance(obj, cls) for cls in self.VALID_TARGETS_CLASSES]):
            # if isinstance(obj, Invader) or isinstance(obj, InvaderShot):

            # Calculate damage based on critical hit chance
            damage = self.DAMAGE
            if np.random.default_rng().random() <= self.CRITICAL_HIT_CHANCE:
                damage *= 2
                print(self, ": critical hit!")

            self.scene.game.traumatize(0.1 * damage)

            obj.hit(damage=damage, by=self)
            if obj.hit_points <= 0:
                self.scene.game.score += obj.SCORE
            self.frame = 2


class HeroWeapon(Weapon):
    """Base class for hero weapons"""
    pass
