from objects.game_object import GameObject
from objects.position import Position
from objects.game_object import Sprite
from objects.explosion import Explosion

from scenes.scene import Scene


class Vehicle(GameObject):
    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)
        self.pos = pos
        self.sprite = sprite
        self.is_active = True

    def draw(self, camera):
        pass

    def update(self, dt):
        pass

    def destroy(self, explode=False):
        super().destroy()
        if explode:
            Explosion(scene=self.scene, pos=self.pos, scale=8)

