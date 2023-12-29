import random

import pygame
from collections import namedtuple


SCREEN_SIZE = (800, 600)
BG_COLOR = (0, 0, 0)
FPS_CAP = 120

HERO_SPEED = 200
HERO_ANIMATION_FPS = 6

ENEMY_SPEED = 10
ENEMY_ANIMATION_FPS = 2

EXPLOSION_ANIMATION_FPS = 6


Sprite = namedtuple("Sprite", ["frames", "width", "height"])


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float):
        return Position(self.x * other, self.y * other)

    def __truediv__(self, other: float):
        return Position(self.x / other, self.y / other)

    def get_normalized(self):
        return Position(self.x / self.get_length(), self.y / self.get_length())

    def get_length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


class GameObject:
    def __init__(self):
        self.destroyed = False
        GameObject.objects.append(self)

    def __del__(self):
        self.destroy()

    def draw(self, surface):
        pass

    def update(self, dt):
        pass

    def destroy(self):
        self.destroyed = True

    @staticmethod
    def draw_all(surface):
        for obj in GameObject.objects:
            obj.draw(surface)

    @staticmethod
    def update_all(dt):
        GameObject.objects = [obj for obj in GameObject.objects if not obj.destroyed]
        for obj in GameObject.objects:
            obj.update(dt)


GameObject.objects = []


class Character(GameObject):
    def __init__(self, pos: Position, sprite: Sprite):
        super().__init__()
        self.pos = pos
        self.sprite = sprite

    def draw(self, surface):
        surface.blit(
            self.sprite.frames[round(HERO_ANIMATION_FPS * total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos)
        )

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos.x -= HERO_SPEED * dt / 1000
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos.x += HERO_SPEED * dt / 1000

        # Hero will appear from another side of the screen if he goes out of bounds
        if self.pos.x < 0:
            self.pos.x = screen_size[0] - self.sprite.width
        elif self.pos.x > screen_size[0] - self.sprite.width:
            self.pos.x = 0


class Enemy(GameObject):
    SCORE = 100

    def __init__(self, pos: Position, sprite: Sprite):
        super().__init__()
        self.pos = pos
        self.sprite = sprite

    def draw(self, surface):
        surface.blit(
            self.sprite.frames[round(ENEMY_ANIMATION_FPS * total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos)
        )

    def update(self, dt):
        self.pos.y += ENEMY_SPEED * dt / 1000


class Explosion(GameObject):
    def __init__(self, pos: Position):
        explosion_sprite = Sprite(
            frames=get_frames(pygame.image.load("assets/images/explosion.png"), 40, 40, 6),
            width=40,
            height=40
        )

        super().__init__()
        self.pos = pos
        self.sprite = explosion_sprite
        self.frame = 0
        self.start_time = pygame.time.get_ticks()

        # Plays a random explosion sound
        pygame.mixer.Sound(f"assets/audio/explosions/exp{random.randint(0, 8)}.wav").play()

    def draw(self, surface):
        if self.frame < len(self.sprite.frames):
            surface.blit(self.sprite.frames[self.frame], tuple(self.pos))

    def update(self, dt):
        self.frame = round(EXPLOSION_ANIMATION_FPS * (pygame.time.get_ticks() - self.start_time) / 1000)
        if self.frame >= len(self.sprite.frames):
            self.destroy()


class Shot(GameObject):
    SHOT_LENGTH = 10

    def __init__(self, pos: Position, velocity: Position, color: tuple):
        super().__init__()
        self.pos = pos
        self.velocity = velocity
        self.color = color

        self.direction = self.velocity.get_normalized() * Shot.SHOT_LENGTH

        # Plays sound BLASTER_Deep_Muffled_stereo.wav
        pygame.mixer.Sound("assets/audio/BLASTER_Deep_Muffled_stereo.wav").play()

    def draw(self, surface):
        pygame.draw.line(surface, self.color, tuple(self.pos), tuple(self.pos + self.direction), 2)

    def update(self, dt):
        global score

        self.pos += self.velocity * dt / 1000

        if self.pos.y < 0:
            self.destroy()

        for enemy in GameObject.objects:
            if (isinstance(enemy, Enemy) and enemy.pos.x <= self.pos.x <= enemy.pos.x + enemy.sprite.width
                    and enemy.pos.y <= self.pos.y <= enemy.pos.y + enemy.sprite.height):
                score += Enemy.SCORE
                Explosion(pos=enemy.pos)
                enemy.destroy()
                self.destroy()


def get_frames(spritesheet, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        # Get the frame from the sprite sheet with the specified width, height and position§
        frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames


def init_enemies():
    sprite = Sprite(frames=get_frames(pygame.image.load("assets/images/invader.png"), 40, 40, 2), width=40, height=40)
    enemies = []
    for row in range(3):
        for col in range(10):
            enemies.append(
                Enemy(
                    pos=Position(100 + col * (sprite.width + 100), 100 + 100 * row),
                    sprite=sprite
                )
            )


def init_font():
    pygame.font.init()
    font = pygame.font.Font("assets/fonts/Revamped.otf", 18)
    return font


def show_stats(screen, clock):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, pygame.Color("lime"))
    screen.blit(fps_text, (8, 8))

    score_text = font.render(str(score), True, pygame.Color("lime"))
    screen.blit(score_text, (screen_size[0] / 2 - score_text.get_width() / 2, 8))

    objects_text = font.render(str(len(GameObject.objects)), True, pygame.Color("lime"))
    screen.blit(objects_text, (screen_size[0] - objects_text.get_width() - 8, 8))


if __name__ == '__main__':
    score = 0
    font = init_font()

    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Set window title and icon
    pygame.display.set_caption("Space Invaders")
    pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))

    screen_size = pygame.display.get_surface().get_size()
    screen_center = screen_size[0] / 2, screen_size[1] / 2

    sprite = Sprite(frames=get_frames(pygame.image.load("assets/images/hero.png"), 32, 32, 6), width=32, height=32)
    hero = Character(
        Position(x=screen_center[0], y=screen_size[1] - sprite.height - 32),
        sprite=sprite
    )

    init_enemies()

    clock = pygame.time.Clock()

    start_time = pygame.time.get_ticks()

    loop = True
    while loop:
        dt = clock.tick(FPS_CAP)
        total_time = pygame.time.get_ticks() - start_time

        screen.fill(BG_COLOR)

        GameObject.update_all(dt)
        GameObject.draw_all(screen)
        show_stats(screen, clock)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = False
                elif event.key == pygame.K_SPACE:
                    Shot(
                        pos=hero.pos + Position(hero.sprite.width / 2, hero.sprite.height / 2),
                        velocity=Position(0, -300),
                        color=(255, 255, 255)
                    )

        pygame.display.flip()

    pygame.quit()