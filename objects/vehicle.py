from objects.explodable_rigid_body import ExplodableRigidBody
from objects.position import Position
from objects.game_object import Sprite

from scenes.scene import Scene


class Vehicle(ExplodableRigidBody):
    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene, pos, sprite)
