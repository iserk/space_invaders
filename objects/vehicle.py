from objects.explodable_rigid_body import ExplodableRigidBody
from objects.position import Position
from objects.game_object import Sprite

from scenes.scene import Scene


class Vehicle(ExplodableRigidBody):
    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene, pos, sprite)

    def draw(self, camera):
        super().draw(camera)

    def update(self, dt):
        super().update(dt)

    def hit(self, damage=1, obj=None):
        super().hit(damage, obj)

    def collide(self, obj=None):
        super().collide(obj)

    def detect_collisions(self):
        super().detect_collisions()

    def destroy(self, explode=False):
        super().destroy(explode)

