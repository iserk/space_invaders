import random
import pygame
from pygame import Vector2

from utils import audio

from objects.position import Position
from weapons.hero_shot import HeroWeapon, HeroShot
from scenes.scene import Scene


class LaserShot(HeroShot):
    SCORE_COST = 1
    DAMAGE = 4
    PULSE_DURATION = 200

    CRITICAL_HIT_CHANCE = 0.05

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 1.5
    AGAINST_ARMOR = 0.4
    AGAINST_HULL = 0.75

    SHIELD_PIERCING = 0  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0  # Percentage of initial damage that goes through to hull

    def __init__(self, scene: Scene, pos: Position, velocity: Position, weapon=None):
        super().__init__(scene, pos, velocity)

        self.weapon = weapon
        self.start_time = self.scene.game.total_time

        # self.scale = scale
        # image = pygame.image.load("assets/images/hero_shot.png").convert_alpha()
        # image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        #
        # self.sprite = Sprite(
        #     frames=get_frames(
        #         image, 32 * scale, 32 * scale, 3),
        #     width=32 * scale,
        #     height=32 * scale,
        # )

        # self.scene.game.traumatize(0.1)

    def draw(self, camera):
        # super().draw(camera)

        pygame.draw.line(
            camera.screen,
            (128, 128, 64),
            tuple(self.pos),
            tuple(self.pos + Position(0, -1000)),
            4
        )

        # # print(self.get_collider())
        # r = (
        #         min(self.get_rect()[0].x, self.get_rect()[1].x),
        #         min(self.get_rect()[0].y, self.get_rect()[1].y),
        #         abs(self.get_rect()[1].x - self.get_rect()[0].x),
        #         abs(self.get_rect()[1].y - self.get_rect()[0].y) + 2,
        #     )
        # print(__class__.__name__, r)
        #
        # # Draw red box around the collider
        # pygame.draw.rect(
        #     camera.screen,
        #     (255, 0, 0),
        #     r,
        #     1
        # )

        if self.frame == 0:
            self.frame = 1

    def update(self, dt):
        # Forces the shoot to display the 0 frame from the start position
        super().update(dt)

        self.pos = self.scene.hero.pos.copy()

        if self.frame == 2:
            if self.scene.game.total_time - self.start_time > self.PULSE_DURATION:
                self.destroy()
            return

        if self.pos.y < 0 or self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()
            return

        self.detect_collisions()

        self.frame = 2

    def get_rect(self):
        return [
            Vector2(self.pos.x - 8, self.pos.y),
            Vector2(self.pos.x + 8, self.pos.y - 1000),
        ]

    # def on_collision(self, obj=None):
    #     if isinstance(obj, Invader) or isinstance(obj, InvaderShot):
    #         self.scene.game.traumatize(0.2)
    #         obj.hit(damage=self.DAMAGE, by=self)
    #         if obj.hit_points <= 0:
    #             self.scene.game.score += obj.SCORE
    #         # self.frame = 2

    # def destroy(self):
    #     if self.weapon is not None and self.weapon.sound is not None:
    #         self.weapon.sound.stop()
    #     super().destroy()


class Laser(HeroWeapon):
    SPEED = 1
    SHOOT_DELAY = 500
    PELLETS = 1
    ACCURACY = 1

    CLIP_SIZE = 1
    RELOAD_TIME = 1000
    MAX_AMMO = 20

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = LaserShot
        self.sound = None

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity)

        sound = audio.sound(f"assets/audio/beam_shot.wav").play()
        self.vehicle.scene.add_timer(500, lambda: sound.fadeout(500) if sound is not None else None)


