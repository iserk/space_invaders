from pygame import Vector2

from objects.explodable_rigid_body import ExplodableRigidBody
from objects.game_object import Sprite

from scenes.scene import Scene


class Vehicle(ExplodableRigidBody):
    SPEED = 300

    def __init__(self, scene: Scene, pos: Vector2, sprite: Sprite):
        super().__init__(scene, pos, sprite)
        self.weapon = None

    def update(self, dt):
        super().update(dt)

        if self.shield < self.MAX_SHIELD:
            self.shield += dt / 1000 * self.MAX_SHIELD / 10
            if self.shield > self.MAX_SHIELD:
                self.shield = self.MAX_SHIELD

        if self.weapon:
            self.weapon.update(dt)

    def shoot(self):
        if self.weapon:
            self.weapon.shoot(
                scene=self.scene,
                pos=self.pos + Vector2(0, -self.sprite.height / 2),
                velocity=Vector2(0, -self.weapon.SPEED),
            )