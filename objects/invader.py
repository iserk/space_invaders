import random
import math

from utils.draw import draw_health_bar
from utils.noise import fractal_noise
from objects.invader_shot import InvaderShot

from objects.position import Position
from objects.game_object import Sprite
from objects.vehicle import Vehicle
from objects.explosion import Explosion
from scenes.scene import Scene
from game.game_manager import GameStatus, SceneSwitchException


class Invader(Vehicle):
    # SPEED = 10
    SPEED = 0
    ANIMATION_FPS = 2
    MAX_HIT_POINTS = 100
    SCORE = 10 * MAX_HIT_POINTS
    MAX_ARMOR = 10
    MAX_SHIELD = 10

    is_shooting = False
    is_wobbling = False

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene, pos, sprite)

        self.hit_points = self.MAX_HIT_POINTS
        self.armor = self.MAX_ARMOR
        self.shield = self.MAX_SHIELD
        self.initial_pos = pos.copy()
        self.velocity = Position(0, Invader.SPEED)

    def draw(self, camera):
        super().draw(camera)

        # # Draw rectangle around the invader
        #
        # pygame.draw.rect(
        #     camera.screen,
        #     (255, 0, 0),
        #     (
        #         self.pos.x - self.sprite.width / 2,
        #         self.pos.y - self.sprite.height / 2,
        #         self.sprite.width,
        #         self.sprite.height,
        #     ),
        #     1
        # )

        # draw_health_bar(surface, x, y, width, height, color, value, max_value, value_threshold=0)
        draw_health_bar(
            camera.screen,
            self.pos.x - self.sprite.width / 2,
            self.pos.y - self.sprite.height / 2,
            self.sprite.width,
            2,
            (0, 255, 0),
            value=self.hit_points,
            max_value=self.MAX_HIT_POINTS,
            value_threshold=1
        )
        draw_health_bar(
            camera.screen,
            self.pos.x - self.sprite.width / 2,
            self.pos.y - self.sprite.height / 2 - 4,
            self.sprite.width,
            2,
            (160, 160, 160),
            self.armor,
            self.MAX_ARMOR
        )
        draw_health_bar(
            camera.screen,
            self.pos.x - self.sprite.width / 2,
            self.pos.y - self.sprite.height / 2 - 8,
            self.sprite.width,
            2,
            (0, 128, 255),
            self.shield, self.MAX_SHIELD
        )

        # # Drawing armor
        # if self.MAX_ARMOR > 10:
        #     pygame.draw.rect(
        #         camera.screen,
        #         (0, 128, 255),
        #         (
        #             self.pos.x - self.sprite.width / 2,
        #             self.pos.y - self.sprite.height / 2 - 14,
        #             self.sprite.width * self.armor / self.MAX_HIT_POINTS,
        #             2,
        #         )
        #     )
        # elif self.MAX_ARMOR > 1:
        #     for i in range(self.armor):
        #         pygame.draw.rect(
        #             camera.screen,
        #             (0, 128, 255),
        #             (
        #                 self.pos.x - self.sprite.width / 2 + i * self.sprite.width / self.MAX_HIT_POINTS + 2,
        #                 self.pos.y - self.sprite.height / 2 - 14,
        #                 self.sprite.width / self.MAX_HIT_POINTS - 2,
        #                 2,
        #             )
        #         )

        # # Draw a blue circle around the invader to indicate its health (as shields)
        # for i in range(self.hit_points - 1):
        #     pygame.draw.circle(
        #         camera.screen,
        #         (64, 80, 255),
        #         (round(self.pos.x), round(self.pos.y)),
        #         self.sprite.width / 2 + 8 + 4 * i,
        #         2
        #     )

    def update(self, dt):
        super().update(dt)

        self.frame = round(Invader.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)

        if self.is_active and self.is_wobbling:
            # self.pos.x = self.initial_pos.x + round(math.sin(self.pos.y / 8) * 40)
            self.velocity.x = round(math.sin(self.pos.y / 8) * self.SPEED * 2)

        if (self.pos.y > self.scene.game.screen_size[1] - self.sprite.height
                and self.scene.game.status == GameStatus.PLAYING):
            raise SceneSwitchException(self.scene.game.scenes[1])
            # self.scene.game.switch_to_scene(self.scene.game.scenes[1])
            # return

        if self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()

        if (self.is_active and self.is_shooting
                and fractal_noise(self.scene.total_time / 1000 + self.pos.x + self.pos.y, 5, 1) > 0.5
                and self.scene.total_time % 1000 < 20):
            InvaderShot(
                scene=self.scene,
                pos=self.pos + Position(0, self.sprite.height / 2),
                velocity=Position(0, InvaderShot.SPEED),
            )
            # pass

    def explode(self):
        Explosion(scene=self.scene, pos=self.pos, scale=random.randint(2, 8))
