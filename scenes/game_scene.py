import random
from collections import namedtuple

import pygame

import settings
from scenes.scene import Scene
from game.game_manager import GameManager, GameStatus
from objects.hero import Hero
from objects.invader import Invader
from objects.position import Position
from objects.game_object import Sprite
from scenes.star_scene import StarScene
from utils import audio
from utils.sprites import get_frames


class GameScene(StarScene):
    STAR_SPEED = 100

    def __init__(self, game: GameManager):
        super().__init__(game)
        self.is_input_enabled = True
        self.total_time = 0
        self.hero = None

    def update(self, dt):
        super().update(dt)
        self.bonus_time_left -= dt

        if len([obj for obj in self.objects if isinstance(obj, Invader)]) == 0:
            self.game.switch_to_scene(self.game.scenes[2])

    def handle_event(self, event):
        for obj in self.objects:
            # If the event was handled, we can skip the rest of the loop
            if not obj.handle_event(event):
                return False
        return True

    def activate(self):
        super().activate()
        self.objects = []
        self.timers = []
        self.game.score = 0
        self.bonus_time_left = self.game.BONUS_TIME_LIMIT

        image = pygame.image.load("assets/images/hero.png")
        scale = 2
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        sprite = Sprite(frames=get_frames(image, 32 * scale, 32 * scale, 6), width=32 * scale, height=32 * scale)
        self.hero = Hero(
            scene=self,
            pos=Position(x=self.game.screen_center[0], y=self.game.screen_size[1] - sprite.height - 32),
            sprite=sprite
        )

        sprite = Sprite(frames=get_frames(pygame.image.load("assets/images/invader.png"), 40, 40, 2), width=40,
                        height=40)
        for row in range(4):
            for col in range(10):
                obj = Invader(
                    scene=self,
                    pos=Position(70 + col * (sprite.width + 50), 100 + 80 * row),
                    sprite=sprite
                )
                obj.shield = obj.MAX_SHIELD = max(0, 2 - row)
                obj.armor = obj.MAX_ARMOR = max(0, 3 - row)
                obj.hit_points = obj.MAX_HIT_POINTS = max(0, row + 1)

        self.game.status = GameStatus.PLAYING
        audio.music("assets/audio/combat_music.wav").play(loops=-1)

