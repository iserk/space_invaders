import random

from pygame import Vector2

from objects.explosion_effect import ExplosionEffect
from objects.rigid_body import RigidBody


class ExplodableRigidBody(RigidBody):

    DETONATION_CHANCE = 0.5
    EXPLOSION_DAMAGE = 100

    @staticmethod
    def get_detonation_delay():
        return random.randint(20, 300)

    def will_destroy(self, by: RigidBody = None):
        print("will_destroy", self, by)
        velocity_y_sign = 1 if by.velocity.y >= 0 else -1

        torque = (self.pos.x - by.pos.x) / self.sprite.width / 2 * velocity_y_sign if self.sprite is not None else 0
        # torque = (self.pos.x - by.pos.x) / self.sprite.width / 2 * velocity_y_sign

        self.scene.add_timer(
            self.get_detonation_delay(),
            lambda o=self: o.destroy(explode=self.DETONATION_CHANCE > random.random())
        )
        self.roll = torque * 60
        self.roll_speed = torque * 360
        if by.velocity.length() > 0:
            self.velocity = by.velocity.normalize() * 10
        self.pos.y += (1 - torque) * velocity_y_sign * 10

    def explode(self):
        from weapons.explosion import Explosion

        if random.random() < self.DETONATION_CHANCE:
            Explosion(self.scene, self.pos, damage=self.EXPLOSION_DAMAGE)
        else:
            ExplosionEffect(scene=self.scene, pos=self.pos, scale=random.randint(2, 8))

    def destroy(self, explode=False):
        super().destroy()
        if explode:
            self.explode()

