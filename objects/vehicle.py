from objects.explodable_rigid_body import ExplodableRigidBody
from objects.position import Position
from objects.game_object import Sprite

from scenes.scene import Scene


class Vehicle(ExplodableRigidBody):
    SPEED = 300

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene, pos, sprite)
        self.weapon = None

    def shoot(self):
        if self.weapon:
            # self.weapon.shoot(
            #     scene=self.scene,
            #     pos=self.pos + Position(0, -self.sprite.height / 2),
            #     velocity=Position(0, self.weapon.shot.SPEED),
            # )
            self.weapon.shoot(
                scene=self.scene,
                pos=self.pos + Position(0, -self.sprite.height / 2),
                velocity=Position(0, -self.weapon.SPEED),
            )