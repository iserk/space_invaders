import random
from collections import namedtuple

import pygame
from pygame import Vector2

import settings
from game.game_manager import GameManager
from scenes.scene import Scene


Star = namedtuple("Star", ["pos", "size", "color"])


class StarScene(Scene):
    STAR_SPEED = 30

    def __init__(self, game: GameManager):
        super().__init__(game)

        self.stars = [
            Star(
                pos=Vector2(x=random.randint(0, self.camera.screen_size[0]), y=random.randint(0, self.camera.screen_size[0])),
                color=(random.randint(32, 255), random.randint(32, 255), random.randint(32, 255)) if random.randint(1, 10) > 5 else (255, 255, 255),
                # color=((255, 255, 255)),
                size=random.randint(0, 2)
             ) for _ in range(100)]

    def update(self, dt):
        super().update(dt)

        for star in self.stars:
            star.pos.y += self.STAR_SPEED * dt / settings.TIME_UNITS_PER_SECOND
            if star.pos.y > self.camera.screen_size[1]:
                star.pos.y = star.pos.y % self.camera.screen_size[1]
                star.pos.x = random.randint(0, self.camera.screen_size[0])

    def draw(self):
        for star in self.stars:
            if star.size == 0:
                self.camera.screen.set_at((round(star.pos.x), round(star.pos.y)), star.color)
            else:
                pygame.draw.circle(self.camera.screen, star.color, (round(star.pos.x), round(star.pos.y)), star.size)
        super().draw()