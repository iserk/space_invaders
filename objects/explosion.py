import random

import pygame

from objects.position import Position
from objects.game_object import GameObject, Sprite
from utils.sprites import get_frames
from scenes.scene import Scene


class Explosion(GameObject):
    ANIMATION_FPS = 6
    ALPHA = 64

    def __init__(self, scene: Scene, pos: Position, scale=2):
        super().__init__(scene)

        self.scale = scale

        # sleep for 20 ms to emphasize the effect
        # pygame.time.wait(20)

        image = pygame.image.load("assets/images/explosion.png").convert_alpha()
        image.set_alpha(round(255 / scale))
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        explosion_sprite = Sprite(
            frames=get_frames(
                image, 40 * scale, 40 * scale, 6),
            width=40 * scale,
            height=40 * scale
        )

        self.pos = pos
        self.sprite = explosion_sprite
        self.frame = 0
        self.start_time = self.scene.game.total_time

        self.scene.game.traumatize(0.8)
        # Plays a random explosion sound

        variants = range(0, 9)
        scales = range(2, 9)
        if self.scale == scales[0]:
            variant = random.choice(variants[0:3])
        else:
            variant = self.scale

        pygame.mixer.Sound(f"assets/audio/explosions/exp{variant}.wav").play()

    def draw(self, camera):
        if self.frame < len(self.sprite.frames):
            camera.screen.blit(self.sprite.frames[self.frame], tuple(self.pos - Position(self.sprite.width / 2, self.sprite.height / 2)))

    def update(self, dt):
        self.frame = round(Explosion.ANIMATION_FPS * (self.scene.game.total_time - self.start_time) / 1000)
        if self.frame >= len(self.sprite.frames):
            self.destroy()

