import math
import random
import enum

import pygame
from collections import namedtuple


SCREEN_SIZE = (800, 600)
BG_COLOR = (0, 0, 0)
FPS_CAP = 120


Sprite = namedtuple("Sprite", ["frames", "width", "height"])


class GameStatus(enum.Enum):
    PLAYING = 0
    VICTORY = 1
    DEFEAT = 2


class GameManager:
    def __init__(self):
        self.score = 0
        self.scenes = []
        self.current_scene = None
        self.status = GameStatus.PLAYING

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        # Set window title and icon
        pygame.display.set_caption("Space Invaders")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))

        self.screen_size = pygame.display.get_surface().get_size()
        self.screen_center = self.screen_size[0] / 2, self.screen_size[1] / 2

        pygame.font.init()
        self.font = pygame.font.Font("assets/fonts/Revamped.otf", 18)

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.is_running = True

    def switch_to_scene(self, scene):
        if self.current_scene is not None:
            scene.objects = self.current_scene.objects.copy()
            self.current_scene.deactivate()
        self.current_scene = scene
        scene.activate()

    def update(self, dt):
        self.current_scene.update(dt)

    def handle_events(self):
        for event in pygame.event.get():
            # Handle events for the current scene
            # If the scene returns False, it means that the event was handled and we can skip the rest of the loop
            if not self.current_scene.handle_event(event):
                continue
            if event.type == pygame.QUIT:
                game.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.is_running = False

    def draw(self, surface):
        self.current_scene.draw(surface)


class Scene:
    def __init__(self, game: GameManager):
        self.game = game
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        obj.scene = self

    def show_stats(self, screen, clock):
        fps = str(int(clock.get_fps()))
        fps_text = self.game.font.render(fps, True, pygame.Color("lime"))
        screen.blit(fps_text, (8, 8))

        score_text = self.game.font.render(str(self.game.score), True, pygame.Color("lime"))
        screen.blit(score_text, (self.game.screen_size[0] / 2 - score_text.get_width() / 2, 8))

        objects_text = self.game.font.render(str(len(self.objects)), True, pygame.Color("lime"))
        screen.blit(objects_text, (self.game.screen_size[0] - objects_text.get_width() - 8, 8))

        match self.game.status:
            case GameStatus.DEFEAT:
                game_over_text = self.game.font.render("GAME OVER", True, pygame.Color("red"))
                screen.blit(game_over_text, (self.game.screen_size[0] / 2 - game_over_text.get_width() / 2, self.game.screen_size[1] / 2))
            case GameStatus.VICTORY:
                victory_text = self.game.font.render("VICTORY", True, pygame.Color("lime"))
                screen.blit(victory_text, (self.game.screen_size[0] / 2 - victory_text.get_width() / 2, self.game.screen_size[1] / 2))

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)
        self.show_stats(surface, self.game.clock)

    def update(self, dt):
        self.objects = [obj for obj in self.objects if not obj.destroyed]
        for obj in self.objects:
            obj.update(dt)

    def handle_event(self, event):
        return True

    def activate(self):
        pass

    def deactivate(self):
        pass


class GameScene(Scene):
    def __init__(self, game: GameManager):
        super().__init__(game)

        sprite = Sprite(frames=get_frames(pygame.image.load("assets/images/hero.png"), 32, 32, 6), width=32, height=32)
        self.hero = Character(
            scene=self,
            pos=Position(x=self.game.screen_center[0], y=self.game.screen_size[1] - sprite.height - 32),
            sprite=sprite
        )

        sprite = Sprite(frames=get_frames(pygame.image.load("assets/images/invader.png"), 40, 40, 2), width=40,
                        height=40)
        for row in range(3):
            for col in range(8):
                Enemy(
                    scene=self,
                    pos=Position(70 + col * (sprite.width + 50), 100 + 80 * row),
                    sprite=sprite
                )

        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        super().update(dt)
        print(self.game.status)
        if len([obj for obj in self.objects if isinstance(obj, Enemy)]) == 0:
            self.game.switch_to_scene(self.game.scenes[2])

    def draw(self, surface):
        super().draw(surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                HeroShot(
                    scene=self,
                    pos=self.hero.pos + Position(self.hero.sprite.width / 2, self.hero.sprite.height / 2),
                    velocity=Position(0, -300),
                )
                # return False
        return True

    def activate(self):
        self.game.status = GameStatus.PLAYING
        pygame.mixer.init()
        pygame.mixer.music.load("assets/audio/Enemies.wav")
        pygame.mixer.music.play(loops=-1)


class DefeatScene(Scene):
    def __init__(self, game: GameManager):
        super().__init__(game)

    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        super().draw(surface)

    def activate(self):
        self.game.status = GameStatus.DEFEAT
        pygame.mixer.music.load("assets/audio/defeat.wav")
        pygame.mixer.music.play()


class VictoryScene(Scene):
    def __init__(self, game: GameManager):
        super().__init__(game)

    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        super().draw(surface)

        score_text = self.game.font.render(str(self.game.score), True, pygame.Color("lime"))
        self.game.screen.blit(score_text, (self.game.screen_size[0] / 2 - score_text.get_width() / 2, 8))

        victory_text = self.game.font.render("VICTORY", True, pygame.Color("lime"))
        self.game.screen.blit(victory_text,
                    (self.game.screen_size[0] / 2 - victory_text.get_width() / 2, self.game.screen_size[1] / 2))

    def activate(self):
        self.game.status = GameStatus.VICTORY
        pygame.mixer.music.load("assets/audio/victory.wav")
        pygame.mixer.music.play()


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Position(x={self.x}, y={self.y})"

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

    def copy(self):
        return Position(self.x, self.y)


class GameObject:
    def __init__(self, scene: Scene):
        self.scene = scene
        self.scene.add(self)
        self.destroyed = False

    def draw(self, surface):
        pass

    def update(self, dt):
        pass

    def destroy(self):
        self.destroyed = True


class Character(GameObject):
    SPEED = 200
    ANIMATION_FPS = 6

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)
        self.pos = pos
        self.sprite = sprite

    def draw(self, surface):
        surface.blit(
            self.sprite.frames[round(Character.ANIMATION_FPS * total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos)
        )

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos.x -= Character.SPEED * dt / 1000
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos.x += Character.SPEED * dt / 1000

        # Hero will appear from another side of the screen if he goes out of bounds
        if self.pos.x < 0:
            self.pos.x = self.scene.game.screen_size[0] - self.sprite.width
        elif self.pos.x > self.scene.game.screen_size[0] - self.sprite.width:
            self.pos.x = 0

    def destroy(self):
        super().destroy()
        self.scene.game.switch_to_scene(self.scene.game.scenes[1])


class Enemy(GameObject):
    SPEED = 10
    ANIMATION_FPS = 2
    SCORE = 100

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)
        self.pos = pos
        self.sprite = sprite

        self.initial_pos = pos.copy()

    def draw(self, surface):
        surface.blit(
            self.sprite.frames[round(Enemy.ANIMATION_FPS * total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos)
        )

    def update(self, dt):
        self.pos.y += Enemy.SPEED * dt / 1000
        self.pos.x = self.initial_pos.x + round(math.sin(self.pos.y / 4) * 40)

        if (self.pos.y > self.scene.game.screen_size[1] - self.sprite.height
                and self.scene.game.status == GameStatus.PLAYING):

            self.scene.game.switch_to_scene(self.scene.game.scenes[1])

        if self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()

        if random.randint(0, 10000) < 5:
            InvaderShot(
                scene=self.scene,
                pos=self.pos + Position(self.sprite.width / 2, self.sprite.height),
                velocity=Position(0, 200),
            )


class Explosion(GameObject):
    ANIMATION_FPS = 6

    def __init__(self, scene: Scene, pos: Position):
        super().__init__(scene)

        explosion_sprite = Sprite(
            frames=get_frames(pygame.image.load("assets/images/explosion.png"), 40, 40, 6),
            width=40,
            height=40
        )

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
        self.frame = round(Explosion.ANIMATION_FPS * (pygame.time.get_ticks() - self.start_time) / 1000)
        if self.frame >= len(self.sprite.frames):
            self.destroy()


class Shot(GameObject):
    SHOT_LENGTH = 10

    def __init__(self, scene: Scene, pos: Position, velocity: Position, color: tuple):
        super().__init__(scene)
        self.pos = pos
        self.velocity = velocity
        self.color = color

        self.direction = self.velocity.get_normalized() * Shot.SHOT_LENGTH

    def draw(self, surface):
        pygame.draw.line(surface, self.color, tuple(self.pos), tuple(self.pos + self.direction), 2)

    def update(self, dt):
        self.pos += self.velocity * dt / 1000

        if self.pos.y < 0 or self.pos.y > self.scene.game.screen_size[1]:
            self.destroy()


class HeroShot(Shot):
    SCORE_COST = 10
    COLOR = (0, 255, 255)

    def __init__(self, scene: Scene, pos: Position, velocity: Position):
        super().__init__(scene, pos, velocity, HeroShot.COLOR)
        self.scene.game.score -= HeroShot.SCORE_COST
        pygame.mixer.Sound("assets/audio/BLASTER_Deep_Muffled_stereo.wav").play()

    def update(self, dt):
        super().update(dt)

        for enemy in self.scene.objects:
            if (isinstance(enemy, Enemy) and enemy.pos.x <= self.pos.x <= enemy.pos.x + enemy.sprite.width
                    and enemy.pos.y <= self.pos.y <= enemy.pos.y + enemy.sprite.height):
                self.scene.game.score += Enemy.SCORE
                Explosion(scene=self.scene, pos=enemy.pos)
                enemy.destroy()
                self.destroy()


class InvaderShot(Shot):
    COLOR = (255, 63, 63)

    def __init__(self, scene: Scene, pos: Position, velocity: Position):
        super().__init__(scene, pos, velocity, InvaderShot.COLOR)
        pygame.mixer.Sound(f"assets/audio/invader_shot{random.randint(1, 2)}.wav").play()

    def update(self, dt):
        super().update(dt)

        hero = self.scene.hero
        if (hero.pos.x <= self.pos.x <= hero.pos.x + hero.sprite.width
                and hero.pos.y <= self.pos.y <= hero.pos.y + hero.sprite.height):
            Explosion(scene=self.scene, pos=hero.pos)
            hero.destroy()
            self.destroy()


def get_frames(spritesheet, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        # Get the frame from the sprite sheet with the specified width, height and position§
        frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames


if __name__ == '__main__':
    game = GameManager()
    game.scenes.append(GameScene(game))
    game.scenes.append(DefeatScene(game))
    game.scenes.append(VictoryScene(game))
    game.switch_to_scene(game.scenes[0])

    while game.is_running:
        dt = game.clock.tick(FPS_CAP)
        total_time = pygame.time.get_ticks() - game.start_time

        game.screen.fill(BG_COLOR)
        game.handle_events()
        game.update(dt)
        game.draw(game.screen)

        pygame.display.flip()

    pygame.quit()