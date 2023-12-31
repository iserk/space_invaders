import random

import pygame

from objects.game_object import GameObject
from objects.position import Position
from objects.game_object import Sprite
from objects.explosion import Explosion
from objects.rigid_body import RigidBody

from scenes.scene import Scene


class ExplodableRigidBody(RigidBody):

    @staticmethod
    def get_detonation_delay():
        return random.randint(20, 300)

    def will_destroy(self, by: RigidBody = None):
        velocity_y_sign = 1 if by.velocity.y >= 0 else -1
        torque = (self.pos.x - by.pos.x) / self.sprite.width / 2 * velocity_y_sign

        self.scene.add_timer(self.get_detonation_delay(), lambda o=self: o.destroy(explode=True))
        self.roll = torque * 60
        self.roll_speed = torque * 360
        self.velocity = by.velocity.get_normalized() * 10
        self.pos.y += (1 - torque) * velocity_y_sign * 10

    def explode(self):
        Explosion(scene=self.scene, pos=self.pos, scale=random.randint(1, 2))

    def destroy(self, explode=False):
        super().destroy()
        if explode:
            self.explode()

