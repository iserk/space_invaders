import random

import pygame
from pygame.math import lerp
from pygame import Vector2

from game.game_manager import SceneSwitchException
from objects.explosion import Explosion

from objects.game_object import Sprite
from objects.vehicle import Vehicle
from scenes.scene import Scene
from utils.draw import draw_health_bar, draw_stats
from weapons.plasma_cannon import PlasmaCannon
from weapons.autocannon import Autocannon
from weapons.cannon import Cannon
from weapons.shotgun import Shotgun
from weapons.laser import Laser
from weapons.gatling import Gatling


class Hero(Vehicle):
    SPEED = 300
    ANIMATION_FPS = 6
    MAX_HIT_POINTS = 100
    MAX_SHIELD = 100
    MAX_ARMOR = 100

    def __init__(self, scene: Scene, pos: Vector2, sprite: Sprite):
        super().__init__(scene, pos, sprite)
        self.hit_points = self.MAX_HIT_POINTS
        self.weapons = [
            Cannon(vehicle=self),
            Shotgun(vehicle=self),
            Gatling(vehicle=self),
            Autocannon(vehicle=self),
            Laser(vehicle=self),
            PlasmaCannon(vehicle=self),
        ]
        self.switch_weapon(self.weapons[0])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6].__contains__(event.key):
                self.switch_weapon(self.weapons[event.key - pygame.K_1])
                return False
            else:
                return True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.weapon.stop_shooting()
                return False

    def switch_weapon(self, weapon):
        self.weapon = weapon
        self.weapon.start_reloading()

    def update(self, dt):
        super().update(dt)

        self.frame = round(Hero.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)

        if self.scene.is_input_enabled:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.pos.x -= self.SPEED * self.scene.game.dt / 1000
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.pos.x += self.SPEED * self.scene.game.dt / 1000
            if keys[pygame.K_SPACE]:
                self.shoot()

        # Hero will appear from another side of the screen if he goes out of bounds
        if self.pos.x < 0:
            self.pos.x = self.scene.game.screen_size[0] - self.sprite.width
        elif self.pos.x > self.scene.game.screen_size[0] - self.sprite.width:
            self.pos.x = 0

    def destroy(self, explode=False):
        super().destroy(explode)
        # self.scene.game.time_scale = 1
        self.scene.game.traumatize(1)
        raise SceneSwitchException(self.scene.game.scenes[1])
        # self.scene.game.switch_to_scene(self.scene.game.scenes[1])

    def explode(self):
        Explosion(scene=self.scene, pos=self.pos, scale=12)

    def draw_hud(self, camera):
        if self.weapon.is_reloading and self.weapon.ammo > 0:
            weapon_name = self.scene.game.font.render(
                f"{str(self.weapon)} RELOADING   {self.weapon.clip} / {self.weapon.ammo}",
                True,
                (255, 170, 100)
                # pygame.Color("lime")
            )
            # Draw the weapon charge
            pygame.draw.rect(
                camera.screen,
                (128, 64, 32),
                (
                    camera.screen_size[0] / 2 - weapon_name.get_width() / 2 - 8,
                    camera.screen_size[1] - weapon_name.get_height() - 16,
                    (1 - self.weapon.get_reload_time_left() / self.weapon.RELOAD_TIME) * weapon_name.get_width() + 16,
                    weapon_name.get_height() + 16
                )
            )

        elif self.weapon.ammo == 0 and self.weapon.clip == 0:
            weapon_name = self.scene.game.font.render(
                f"{str(self.weapon)}: Out of ammo   {self.weapon.clip} / {self.weapon.ammo}",
                True,
                (255, 64, 64),
            )
            # Draw the weapon charge
            pygame.draw.rect(
                camera.screen,
                (64, 16, 16),
                (
                    camera.screen_size[0] / 2 - weapon_name.get_width() / 2 - 8,
                    camera.screen_size[1] - weapon_name.get_height() - 16,
                    weapon_name.get_width() + 16,
                    weapon_name.get_height() + 16
                )
            )
        else:
            weapon_name = self.scene.game.font.render(
                f"{str(self.weapon)}: {self.weapon.get_charge() * 100:.0f}%   {self.weapon.clip} / {self.weapon.ammo}",
                True,
                pygame.Color("lime")
            )
            # Draw the weapon charge
            pygame.draw.rect(
                camera.screen,
                (32, 64, 32),
                (
                    camera.screen_size[0] / 2 - weapon_name.get_width() / 2 - 8,
                    camera.screen_size[1] - weapon_name.get_height() - 16,
                    self.weapon.get_charge() * weapon_name.get_width() + 16,
                    weapon_name.get_height() + 16
                )
            )

        camera.screen.blit(weapon_name, (
            camera.screen_size[0] / 2 - weapon_name.get_width() / 2,
            camera.screen_size[1] - weapon_name.get_height() - 8)
                           )

    def draw(self, camera):
        super().draw(camera)
        # Draw a blue circle around the invader to indicate its health (as shields)

        # Draw the health bar
        # draw_stats(self, camera)

        max_shield = 4
        shield = round(self.shield / self.MAX_SHIELD * max_shield)

        for i in range(shield - 1):
            q = (i + 1) / max_shield
            c = (lerp(16, 64, q), lerp(32, 128, q), lerp(64, 255, q))
            color = tuple(map(round, c))
            pygame.draw.circle(
                camera.screen,
                color,
                (round(self.pos.x), round(self.pos.y)),
                self.sprite.width / 2 + 8 + 4 * i,
                2
            )

        self.draw_hud(camera)
