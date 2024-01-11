import random
import pygame
from pygame import Vector2

from utils import audio

from objects.position import Position
from weapons.hero_shot import HeroWeapon, HeroShot
from scenes.scene import Scene
from weapons.shot import ShotState


class LaserShot(HeroShot):
    DESTROY_ON_HIT = False
    SCORE_COST = 1
    DAMAGE = 50
    PULSE_DURATION = 190

    CRITICAL_HIT_CHANCE = 0.05

    # Multipliers against armor, shields and hull
    AGAINST_SHIELD = 1.5
    AGAINST_ARMOR = 0.5
    AGAINST_HULL = 0.75

    SHIELD_PIERCING = 0.50  # Percentage of initial damage that goes through to armor
    ARMOR_PIERCING = 0.00  # Percentage of initial damage that goes through to hull

    def __init__(self, scene: Scene, pos: Position, velocity: Position, weapon=None):
        super().__init__(scene, pos, velocity)

        self.weapon = weapon
        self.start_time = self.scene.game.total_time
        self.affected_targets = []

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

    def on_collision(self, obj=None):
        if not obj.is_active or not any([isinstance(obj, cls) for cls in self.VALID_TARGETS_CLASSES]):
            return

        self.affected_targets.append(obj)
        self.state = ShotState.HITTING

    def draw(self, camera):
        # super().draw(camera)

        pygame.draw.line(
            camera.screen,
            (128, 128, 64),
            tuple(self.pos + Position(-2, -32)),
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

        if self.state == ShotState.STARTING:
            self.state = ShotState.FLYING

    def update(self, dt):
        super().update(dt)

        if (self.state == ShotState.DESTROYED
                or self.pos.y < 0 or self.pos.y > self.scene.game.screen_size[1]
                or self.state == ShotState.HITTING
                and self.scene.game.total_time - self.start_time > self.PULSE_DURATION
        ):
            self.destroy()
            return

        self.pos = self.scene.hero.pos.copy()

        if self.state == ShotState.HITTING:
            for obj in self.affected_targets:
                if not obj.is_active:
                    continue

                # Calculate damage based on critical hit chance
                damage = self.DAMAGE
                self.scene.game.traumatize(0.1 * damage)

                if random.random() <= self.CRITICAL_HIT_CHANCE:
                    damage *= 2
                    print(self, ": critical hit!")

                obj.hit(damage=self.damage * dt / 1000, by=self)

                if obj.hit_points <= 0:
                    self.scene.game.score += obj.SCORE

        self.affected_targets = []

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
    SHOOT_DELAY = 200
    PELLETS = 1
    ACCURACY = 1

    CLIP_SIZE = 1000
    RELOAD_TIME = 1000
    MAX_AMMO = 10000

    def __init__(self, vehicle=None):
        super().__init__(vehicle)
        self.shot = LaserShot
        self.sound = None

    def _perform_shot(self, scene, pos, velocity):
        for _ in range(self.PELLETS):
            super()._send_bullet(scene, pos, velocity)

        sound = audio.sound(f"assets/audio/beam_shot.wav").play()
        self.vehicle.scene.add_timer(500, lambda: sound.fadeout(500) if sound is not None else None)
