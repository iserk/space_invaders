import random

from objects.explodable_rigid_body import ExplodableRigidBody
from objects.position import Position
from scenes.scene import Scene


class Shot(ExplodableRigidBody):
    DAMAGE = 1
    SHOT_LENGTH = 16
    SPEED = 300

    def __init__(self, scene: Scene, pos: Position, velocity: Position):
        super().__init__(scene, pos, None)
        self.pos = pos
        self.velocity = velocity

        self.frame = 0

        self.direction = self.velocity.get_normalized() * Shot.SHOT_LENGTH

    def draw(self, camera):
        super().draw(camera)
        if self.frame == 0:
            self.frame = 1

    def update(self, dt):
        super().update(dt)

        if self.frame == 2:
            self.destroy()
            return

        if self.pos.y < 0 or self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()

    @staticmethod
    def get_detonation_delay():
        return random.randint(20, 100)
