import math
import random
import enum

import pygame
from collections import namedtuple


SCREEN_SIZE = (1000, 800)
BG_COLOR = (0, 0, 0)
FPS_CAP = 120


Sprite = namedtuple("Sprite", ["frames", "width", "height"])


class GameStatus(enum.Enum):
    PLAYING = 0
    VICTORY = 1
    DEFEAT = 2


class SceneSwitchException(Exception):
    pass


class GameManager:
    BONUS_TIME_LIMIT = 15000  # 15 seconds

    def __init__(self):
        self.dt = 0
        self.total_time = 0
        self.score = 0
        self.scenes = []
        self.current_scene = None
        self.status = GameStatus.PLAYING
        self.time_scale = 1

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
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
        self.is_paused = False

    def switch_to_scene(self, scene):
        scene.will_activate(prev_scene=self.current_scene)
        if self.current_scene is not None:
            # scene.objects = self.current_scene.objects.copy()
            self.current_scene.deactivate()
        self.current_scene = scene
        scene.activate()

    def update(self, dt):
        try:
            self.current_scene.update(dt)
        except SceneSwitchException as e:
            self.switch_to_scene(e.args[0])

    def handle_events(self):
        for event in pygame.event.get():
            # Handle events for the current scene
            # If the scene returns False, it means that the event was handled and we can skip the rest of the loop
            if not self.is_paused:
                result = self.current_scene.handle_event(event)
                if not result:
                    continue

            if event.type == pygame.QUIT:
                game.is_running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        game.is_running = False
                    case pygame.K_p:
                        game.is_paused = not game.is_paused
                    case pygame.K_q:
                        game.time_scale = 0.25
                    case pygame.K_w:
                        game.time_scale = 1
                    case pygame.K_e:
                        game.time_scale = 2


    def draw(self, surface):
        self.current_scene.draw(surface)

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Scene:
    def __init__(self, game: GameManager):
        self.game = game
        self.objects = []
        self.total_time = 0
        self.bonus_time_left = 0

    def activate(self):
        # print(f"Activated {self.__class__.__name__}")
        pass

    def add(self, obj):
        self.objects.append(obj)
        obj.scene = self

    def show_stats(self, screen, clock):
        fps = str(int(clock.get_fps()))
        fps_text = self.game.font.render(f'FPS: {fps}', True, pygame.Color("lime"))
        screen.blit(fps_text, (8, 8))

        time_scale_text = self.game.font.render(f'Time: {self.game.time_scale:.2f}x', True, pygame.Color("lime"))
        screen.blit(time_scale_text, (200, 8))

        score_text = self.game.font.render(f"Score: {self.game.score:08}", True, pygame.Color("lime"))
        screen.blit(score_text, (self.game.screen_size[0] / 2 - score_text.get_width() / 2, 8))

        # objects_text = self.game.font.render(f'Objects: {len(self.objects):04}', True, pygame.Color("lime"))
        # screen.blit(objects_text, (self.game.screen_size[0] - objects_text.get_width() - 8, 8))

        time_remaining = max(0, self.bonus_time_left) / 1000

        time_text = self.game.font.render(f'Bonus time: {time_remaining:.1f} s', True, pygame.Color("lime"))
        screen.blit(time_text, (self.game.screen_size[0] - time_text.get_width() - 8, 8))

        if self.game.is_paused:
            pause_text = self.game.font.render('Paused', True, pygame.Color("aqua"))
            screen.blit(pause_text, (self.game.screen_center[0] - pause_text.get_width(), self.game.screen_center[1]))

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

    def will_activate(self, prev_scene=None):
        pass

    def deactivate(self):
        self.objects = []

    def transfer_objects_from(self, scene):
        for obj in scene.objects:
            self.add(obj)

    def __repr__(self):
        return f"{self.__class__.__name__}(game={self.game})"


class GameScene(Scene):
    def __init__(self, game: GameManager):
        super().__init__(game)
        self.total_time = 0

    def update(self, dt):
        super().update(dt)

        self.bonus_time_left -= dt

        if len([obj for obj in self.objects if isinstance(obj, Enemy)]) == 0:
            self.game.switch_to_scene(self.game.scenes[2])

    def draw(self, surface):
        super().draw(surface)

    def handle_event(self, event):
        for obj in self.objects:
            # If the event was handled, we can skip the rest of the loop
            if not obj.handle_event(event):
                return False
        return True

    def activate(self):
        super().activate()
        self.game.score = 0
        self.bonus_time_left = self.game.BONUS_TIME_LIMIT

        sprite = Sprite(frames=get_frames(pygame.image.load("assets/images/hero.png"), 32, 32, 6), width=32, height=32)
        self.hero = Character(
            scene=self,
            pos=Position(x=self.game.screen_center[0], y=self.game.screen_size[1] - sprite.height - 32),
            sprite=sprite
        )

        sprite = Sprite(frames=get_frames(pygame.image.load("assets/images/invader.png"), 40, 40, 2), width=40,
                        height=40)
        for row in range(3):
            for col in range(10):
                Enemy(
                    scene=self,
                    pos=Position(70 + col * (sprite.width + 50), 100 + 80 * row),
                    sprite=sprite
                )

        self.game.status = GameStatus.PLAYING
        pygame.mixer.init()
        pygame.mixer.music.load("assets/audio/combat_music.wav")
        pygame.mixer.music.play(loops=-1)


class DefeatScene(Scene):
    def __init__(self, game: GameManager):
        super().__init__(game)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.switch_to_scene(self.game.scenes[0])
                return False
        return True

    def update(self, dt):
        super().update(dt)

    def draw(self, screen):
        super().draw(screen)
        game_over_text = self.game.font.render("GAME OVER", True, pygame.Color("red"))
        screen.blit(game_over_text, (self.game.screen_size[0] / 2 - game_over_text.get_width() / 2, self.game.screen_size[1] / 2))

        key_text = self.game.font.render("Press <R> to try again, <ESC> to quit", True, pygame.Color("gray"))
        self.game.screen.blit(key_text,
                              (self.game.screen_size[0] / 2 - key_text.get_width() / 2,
                               self.game.screen_size[1] / 2 + 120))

    def will_activate(self, prev_scene=None):
        super().will_activate(prev_scene)

        if prev_scene is not None:
            self.transfer_objects_from(prev_scene)

    def activate(self):
        super().activate()
        self.game.status = GameStatus.DEFEAT
        pygame.mixer.music.load("assets/audio/defeat.wav")
        pygame.mixer.music.play()


class VictoryScene(Scene):
    def __init__(self, game: GameManager):
        super().__init__(game)
        self.time_bonus = 0

    def activate(self):
        super().activate()
        self.game.status = GameStatus.VICTORY
        pygame.mixer.music.load("assets/audio/victory.wav")
        pygame.mixer.music.play()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.switch_to_scene(self.game.scenes[0])
                return False
        return True

    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        super().draw(surface)

        victory_text = self.game.font.render("VICTORY", True, pygame.Color("lime"))
        self.game.screen.blit(victory_text,
                    (self.game.screen_size[0] / 2 - victory_text.get_width() / 2, self.game.screen_size[1] / 2 - 80))

        score_text = self.game.font.render(f"SCORE: {self.game.score}", True, pygame.Color("lime"))
        self.game.screen.blit(score_text,
                              (self.game.screen_size[0] / 2 - score_text.get_width() / 2,
                               self.game.screen_size[1] / 2 - 40))

        time_bonus_text = self.game.font.render(f"TIME BONUS: {self.time_bonus}", True, pygame.Color("lime"))
        self.game.screen.blit(time_bonus_text,
                              (self.game.screen_size[0] / 2 - time_bonus_text.get_width() / 2,
                               self.game.screen_size[1] / 2))

        total_score = self.game.font.render(f"TOTAL SCORE: {self.game.score + self.time_bonus}", True, pygame.Color("lime"))
        self.game.screen.blit(total_score,
                              (self.game.screen_size[0] / 2 - total_score.get_width() / 2,
                               self.game.screen_size[1] / 2 + 40))

        key_text = self.game.font.render("Press <R> to try again, <ESC> to quit", True, pygame.Color("gray"))
        self.game.screen.blit(key_text,
                              (self.game.screen_size[0] / 2 - key_text.get_width() / 2,
                               self.game.screen_size[1] / 2 + 120))

    def will_activate(self, prev_scene=None):
        super().will_activate(prev_scene)

        if prev_scene is not None:
            self.bonus_time_left = prev_scene.bonus_time_left
            self.time_bonus = max(0, self.bonus_time_left)

        if prev_scene is not None:
            self.transfer_objects_from(prev_scene)


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

    def handle_event(self, event):
        """Returns True if the event was not handled and should be passed to the next object"""
        return True

    def destroy(self):
        self.destroyed = True

    def __repr__(self):
        return f"{self.__class__.__name__}(scene={self.scene})"


class Character(GameObject):
    SPEED = 300
    ANIMATION_FPS = 6

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)
        self.pos = pos
        self.sprite = sprite

    def draw(self, surface):
        surface.blit(
            self.sprite.frames[round(Character.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos)
        )

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos.x -= self.SPEED * self.scene.game.dt / 1000
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos.x += self.SPEED * self.scene.game.dt / 1000

        # Hero will appear from another side of the screen if he goes out of bounds
        if self.pos.x < 0:
            self.pos.x = self.scene.game.screen_size[0] - self.sprite.width
        elif self.pos.x > self.scene.game.screen_size[0] - self.sprite.width:
            self.pos.x = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                HeroShot(
                    scene=self.scene,
                    pos=self.pos + Position(self.sprite.width / 2, self.sprite.height / 2),
                    velocity=Position(0, -300),
                )
                return False
        return True

    def destroy(self):
        super().destroy()
        raise SceneSwitchException(self.scene.game.scenes[1])
        # self.scene.game.switch_to_scene(self.scene.game.scenes[1])


class Enemy(GameObject):
    SPEED = 20
    ANIMATION_FPS = 2
    SCORE = 100

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)
        self.pos = pos
        self.sprite = sprite

        self.initial_pos = pos.copy()

    def draw(self, surface):
        surface.blit(
            self.sprite.frames[round(Enemy.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos)
        )

    def update(self, dt):
        self.pos.y += Enemy.SPEED * dt / 1000
        self.pos.x = self.initial_pos.x + round(math.sin(self.pos.y / 8) * 40)

        if (self.pos.y > self.scene.game.screen_size[1] - self.sprite.height
                and self.scene.game.status == GameStatus.PLAYING):

            raise SceneSwitchException(self.scene.game.scenes[1])
            # self.scene.game.switch_to_scene(self.scene.game.scenes[1])
            # return

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
        self.start_time = self.scene.game.total_time

        # Plays a random explosion sound
        pygame.mixer.Sound(f"assets/audio/explosions/exp{random.randint(0, 8)}.wav").play()

    def draw(self, surface):
        if self.frame < len(self.sprite.frames):
            surface.blit(self.sprite.frames[self.frame], tuple(self.pos))

    def update(self, dt):
        self.frame = round(Explosion.ANIMATION_FPS * (self.scene.game.total_time - self.start_time) / 1000)
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
        pygame.mixer.Sound("assets/audio/hero_shot.wav").play()

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

        if hasattr(self.scene, "hero"):
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
        game.dt = round(game.clock.tick(FPS_CAP) * game.time_scale)

        if not game.is_paused:
            # game.total_time = pygame.time.get_ticks() - game.start_time
            game.total_time += game.dt
            game.current_scene.total_time += game.dt

        game.screen.fill(BG_COLOR)
        game.handle_events()

        if not game.is_paused:
            game.update(game.dt)
        game.draw(game.screen)

        pygame.display.flip()

    pygame.quit()