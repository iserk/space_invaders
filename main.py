import math
import random
import enum

import pygame
from collections import namedtuple

from camera import Camera
from noise import fractal_noise


SCREEN_SIZE = (1000, 800)
BG_COLOR = (0, 0, 0)
FPS_CAP = 0


Sprite = namedtuple("Sprite", ["frames", "width", "height"])


class GameStatus(enum.Enum):
    PLAYING = 0
    VICTORY = 1
    DEFEAT = 2


class SceneSwitchException(Exception):
    pass


class GameManager:
    BONUS_TIME_LIMIT = 15000  # 15 seconds
    MAX_TRAUMA = 1
    MIN_TRAUMA = 0

    def __init__(self):
        self.dt = 0
        self.total_time = 0
        self.score = 0
        self.scenes = []
        self.current_scene = None
        self.status = GameStatus.PLAYING
        self.time_scale = 1
        self.use_perlin_noise = True

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF, vsync=True)

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
        self.trauma = 0

    def switch_to_scene(self, scene):
        scene.will_activate(prev_scene=self.current_scene)
        if self.current_scene is not None:
            # scene.objects = self.current_scene.objects.copy()
            self.current_scene.deactivate()
        self.current_scene = scene
        scene.activate()

    def update(self, dt):
        if self.trauma > 0:
            self.trauma -= (dt / 1000)

            amplitude = self.trauma ** 2 * 10

            if self.use_perlin_noise:
                amplitude *= 3
                self.current_scene.camera.x = fractal_noise(self.total_time / 1000, 10, 1) * amplitude
                self.current_scene.camera.y = fractal_noise(self.total_time / 1000 + 1000, 10, 1) * amplitude
                self.current_scene.camera.roll = fractal_noise(self.total_time / 1000 + 2000, 10, 1) * amplitude / 20
            else:
                self.current_scene.camera.x = random.uniform(-amplitude, amplitude)
                self.current_scene.camera.y = random.uniform(-amplitude, amplitude)
                self.current_scene.camera.roll = random.uniform(-amplitude, amplitude) / 20
        else:
            self.trauma = 0

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
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.is_running = False
                    case pygame.K_p:
                        self.is_paused = not self.is_paused
                    case pygame.K_q:
                        self.time_scale = 0.25
                    case pygame.K_w:
                        self.time_scale = 1
                    case pygame.K_e:
                        self.time_scale = 2

                    case pygame.K_1:
                        self.time_scale = 0.1
                    case pygame.K_2:
                        self.time_scale = 0.2
                    case pygame.K_3:
                        self.time_scale = 0.3
                    case pygame.K_4:
                        self.time_scale = 0.4
                    case pygame.K_5:
                        self.time_scale = 0.5
                    case pygame.K_6:
                        self.time_scale = 0.6
                    case pygame.K_7:
                        self.time_scale = 0.7
                    case pygame.K_8:
                        self.time_scale = 0.8
                    case pygame.K_9:
                        self.time_scale = 0.9
                    case pygame.K_0:
                        self.time_scale = 1.0

                    case pygame.K_t:
                        self.traumatize(1)
                    case pygame.K_r:
                        self.switch_to_scene(self.scenes[0])
                    case pygame.K_f:
                        self.use_perlin_noise = not self.use_perlin_noise

    def draw(self):
        self.current_scene.draw()

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def traumatize(self, trauma):
        self.trauma += trauma
        self.trauma = min(self.trauma, self.MAX_TRAUMA)

    def run(self):
        while self.is_running:
            self.dt = round(self.clock.tick(FPS_CAP) * self.time_scale)

            if not self.is_paused:
                # game.total_time = pygame.time.get_ticks() - game.start_time
                self.total_time += self.dt
                self.current_scene.total_time += self.dt

            camera = self.current_scene.camera

            factor = self.trauma ** 2
            camera.screen.fill((64 * factor, 32 * factor, 32 * factor))
            # camera.screen.fill(BG_COLOR)
            self.handle_events()

            if not self.is_paused:
                self.update(game.dt)
            self.draw()

            # camera.x = random.randint(-10, 10)
            # camera.y = random.randint(-10, 10)
            # camera.roll = random.randint(-100, 100) / 100

            # self.screen.blit(camera.transform(), (0, 0))
            camera.display(self.screen)
            pygame.display.flip()

        pygame.quit()


class Scene:
    def __init__(self, game: GameManager):
        self.game = game
        self.objects = []
        self.total_time = 0
        self.bonus_time_left = 0
        self.camera = Camera(self.game.screen_size, 0, 0)
        self.is_input_enabled = False

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

        trauma_text = self.game.font.render(f"{self.game.trauma:.2f}", True, pygame.Color("lime"))
        screen.blit(trauma_text, (8, self.game.screen_size[1] - trauma_text.get_height() - 8))

        # objects_text = self.game.font.render(f'Objects: {len(self.objects):04}', True, pygame.Color("lime"))
        # screen.blit(objects_text, (self.game.screen_size[0] - objects_text.get_width() - 8, 8))

        time_remaining = max(0, self.bonus_time_left) / 1000

        time_text = self.game.font.render(f'Bonus time: {time_remaining:.1f} s', True, pygame.Color("aqua"))
        screen.blit(time_text, (self.game.screen_size[0] - time_text.get_width() - 8, 8))

        noise_text = self.game.font.render('perlin' if self.game.use_perlin_noise else 'random', True, pygame.Color("aqua"))
        screen.blit(noise_text, (self.game.screen_size[0] - noise_text.get_width() - 8, self.game.screen_size[1] - noise_text.get_height() - 8))

        if self.game.is_paused:
            pause_text = self.game.font.render('Paused', True, pygame.Color("aqua"))
            screen.blit(pause_text, (self.game.screen_center[0] - pause_text.get_width(), self.game.screen_center[1]))

    def draw(self):
        for obj in self.objects:
            obj.draw(self.camera)
        self.show_stats(self.camera.screen, self.game.clock)

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
        self.is_input_enabled = True
        self.total_time = 0

    def update(self, dt):
        super().update(dt)

        self.bonus_time_left -= dt

        if len([obj for obj in self.objects if isinstance(obj, Invader)]) == 0:
            self.game.switch_to_scene(self.game.scenes[2])

    def draw(self):
        super().draw()

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
        self.hero = Hero(
            scene=self,
            pos=Position(x=self.game.screen_center[0], y=self.game.screen_size[1] - sprite.height - 32),
            sprite=sprite
        )

        sprite = Sprite(frames=get_frames(pygame.image.load("assets/images/invader.png"), 40, 40, 2), width=40,
                        height=40)
        for row in range(3):
            for col in range(10):
                Invader(
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

    def draw(self,):
        super().draw()
        game_over_text = self.game.font.render("GAME OVER", True, pygame.Color("red"))
        self.camera.screen.blit(game_over_text, (self.game.screen_size[0] / 2 - game_over_text.get_width() / 2, self.game.screen_size[1] / 2))

        key_text = self.game.font.render("Press <R> to try again, <ESC> to quit", True, pygame.Color("gray"))
        self.camera.screen.blit(key_text,
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

    def draw(self):
        super().draw()

        victory_text = self.game.font.render("VICTORY", True, pygame.Color("lime"))
        self.camera.screen.blit(victory_text,
                    (self.game.screen_size[0] / 2 - victory_text.get_width() / 2, self.game.screen_size[1] / 2 - 80))

        score_text = self.game.font.render(f"SCORE: {self.game.score}", True, pygame.Color("lime"))
        self.camera.screen.blit(score_text,
                              (self.game.screen_size[0] / 2 - score_text.get_width() / 2,
                               self.game.screen_size[1] / 2 - 40))

        time_bonus_text = self.game.font.render(f"TIME BONUS: {self.time_bonus}", True, pygame.Color("lime"))
        self.camera.screen.blit(time_bonus_text,
                              (self.game.screen_size[0] / 2 - time_bonus_text.get_width() / 2,
                               self.game.screen_size[1] / 2))

        total_score = self.game.font.render(f"TOTAL SCORE: {self.game.score + self.time_bonus}", True, pygame.Color("lime"))
        self.camera.screen.blit(total_score,
                              (self.game.screen_size[0] / 2 - total_score.get_width() / 2,
                               self.game.screen_size[1] / 2 + 40))

        key_text = self.game.font.render("Press <R> to try again, <ESC> to quit", True, pygame.Color("gray"))
        self.camera.screen.blit(key_text,
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

    def draw(self, camera):
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


class Hero(GameObject):
    SPEED = 300
    ANIMATION_FPS = 6
    SHOOT_DELAY = 200

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)
        self.pos = pos
        self.sprite = sprite
        self.prev_shot_time = 0

    def draw(self, camera):
        camera.screen.blit(
            self.sprite.frames[round(Hero.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos)
        )

    def update(self, dt):

        if self.scene.is_input_enabled:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.pos.x -= self.SPEED * self.scene.game.dt / 1000
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.pos.x += self.SPEED * self.scene.game.dt / 1000
            if keys[pygame.K_SPACE]:
                if self.scene.game.total_time - self.prev_shot_time > self.SHOOT_DELAY:
                    self.prev_shot_time = self.scene.game.total_time
                    HeroShot(
                        scene=self.scene,
                        pos=self.pos + Position(self.sprite.width / 2, self.sprite.height / 2),
                        velocity=Position(0, -HeroShot.SPEED),
                    )

        # Hero will appear from another side of the screen if he goes out of bounds
        if self.pos.x < 0:
            self.pos.x = self.scene.game.screen_size[0] - self.sprite.width
        elif self.pos.x > self.scene.game.screen_size[0] - self.sprite.width:
            self.pos.x = 0

    def destroy(self):
        super().destroy()
        self.scene.game.traumatize(1)
        raise SceneSwitchException(self.scene.game.scenes[1])
        # self.scene.game.switch_to_scene(self.scene.game.scenes[1])


class Invader(GameObject):
    SPEED = 20
    ANIMATION_FPS = 2
    SCORE = 100

    def __init__(self, scene: Scene, pos: Position, sprite: Sprite):
        super().__init__(scene)
        self.pos = pos
        self.sprite = sprite

        self.initial_pos = pos.copy()

    def draw(self, camera):
        camera.screen.blit(
            self.sprite.frames[round(Invader.ANIMATION_FPS * self.scene.game.total_time / 1000) % len(self.sprite.frames)],
            tuple(self.pos)
        )

    def update(self, dt):
        self.pos.y += Invader.SPEED * dt / 1000
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
                velocity=Position(0, InvaderShot.SPEED),
            )


class Explosion(GameObject):
    ANIMATION_FPS = 6

    def __init__(self, scene: Scene, pos: Position):
        super().__init__(scene)

        # sleep for 20 ms to emphasize the effect
        pygame.time.wait(20)

        explosion_sprite = Sprite(
            frames=get_frames(pygame.image.load("assets/images/explosion.png"), 40, 40, 6),
            width=40,
            height=40
        )

        self.pos = pos
        self.sprite = explosion_sprite
        self.frame = 0
        self.start_time = self.scene.game.total_time

        self.scene.game.traumatize(0.8)
        # Plays a random explosion sound
        pygame.mixer.Sound(f"assets/audio/explosions/exp{random.randint(0, 8)}.wav").play()

    def draw(self, camera):
        if self.frame < len(self.sprite.frames):
            camera.screen.blit(self.sprite.frames[self.frame], tuple(self.pos))

    def update(self, dt):
        self.frame = round(Explosion.ANIMATION_FPS * (self.scene.game.total_time - self.start_time) / 1000)
        if self.frame >= len(self.sprite.frames):
            self.destroy()


class Shot(GameObject):
    SHOT_LENGTH = 10
    SPEED = 300

    def __init__(self, scene: Scene, pos: Position, velocity: Position, color: tuple):
        super().__init__(scene)
        self.pos = pos
        self.velocity = velocity
        self.color = color

        self.direction = self.velocity.get_normalized() * Shot.SHOT_LENGTH

    def draw(self, camera):
        pygame.draw.line(camera.screen, self.color, tuple(self.pos), tuple(self.pos + self.direction), 2)

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
        self.scene.game.traumatize(0.1)

    def update(self, dt):
        super().update(dt)

        for enemy in self.scene.objects:
            if (isinstance(enemy, Invader) and enemy.pos.x <= self.pos.x <= enemy.pos.x + enemy.sprite.width
                    and enemy.pos.y <= self.pos.y <= enemy.pos.y + enemy.sprite.height):
                self.scene.game.score += Invader.SCORE
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

    game.run()