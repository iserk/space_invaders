import random

import pygame

from utils import audio
from weapons.weapon import Weapon

from objects.invader_shot import InvaderShot
from objects.shot import Shot
from objects.invader import Invader
from objects.position import Position
from objects.game_object import Sprite
from scenes.scene import Scene

from utils.sprites import get_frames


class AutocannonShot(Shot):
    SCORE_COST = 2
    DAMAGE = 3

    # SHOT_SIZE = (48, 48)

    def __init__(self, scene: Scene, pos: Position, velocity: Position, scale=2):
        # velocity += Position((np.random.default_rng().normal() - 0.5) * self.SPEED * (1 - self.ACCURACY), 0)

        super().__init__(scene, pos, velocity)

        self.scale = scale
        image = pygame.image.load("assets/images/gatling_shot.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

        self.sprite = Sprite(
            frames=get_frames(
                image, 32 * scale, 32 * scale, 3),
            width=32 * scale,
            height=32 * scale,
        )

        # self.scene.game.traumatize(0.1)

        self.frame = 0
        self.scene.game.score -= self.SCORE_COST

    # def draw(self, camera):
    #     super().draw(camera)
    #
    #     pygame.draw.line(
    #         camera.screen,
    #         (128, 128, 64),
    #         tuple(self.prev_pos),
    #         tuple(self.pos),
    #         1
    #     )
    #
    #     # print(self.get_collider())
    #     r = (
    #             min(self.get_collider()[0].x, self.get_collider()[1].x),
    #             min(self.get_collider()[0].y, self.get_collider()[1].y),
    #             abs(self.get_collider()[1].x - self.get_collider()[0].x),
    #             abs(self.get_collider()[1].y - self.get_collider()[0].y) + 2,
    #         )
    #     print(__class__.__name__, r)
    #
    #     # Draw red box around the collider
    #     pygame.draw.rect(
    #         camera.screen,
    #         (255, 0, 0),
    #         r,
    #         1
    #     )

    def on_collision(self, obj=None):
        if self.damage <= 0:
            self.frame = 2
            return

        if isinstance(obj, Invader) or isinstance(obj, InvaderShot) and obj.is_active and obj.hit_points > 0:
            self.scene.game.traumatize(0.2)

            remaining_damage = self.damage - max(0, obj.hit_points)

            # print(f"DMG: {self.damage}, HP: {obj.hit_points}, RD: {remaining_damage}")
            obj.hit(damage=self.damage, by=self)
            if obj.hit_points <= 0:
                self.scene.game.score += obj.SCORE

            self.damage = remaining_damage
            # print(self.damage)
            if self.damage <= 0:
                self.frame = 2


class Autocannon(Weapon):
    SPEED = 3000
    SHOOT_DELAY = 150
    PELLETS = 1
    ACCURACY = 0.8

    CLIP_SIZE = 25
    RELOAD_TIME = 1500
    MAX_AMMO = 100

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = AutocannonShot

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity * random.uniform(0.7, 1.2))

        audio.sound(f"assets/audio/gatling/shot{random.randint(1,4):02}.wav").play()
