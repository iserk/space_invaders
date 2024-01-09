import enum
import random

import pygame

from utils.noise import fractal_noise


class GameStatus(enum.Enum):
    PLAYING = 0
    VICTORY = 1
    DEFEAT = 2


class SceneSwitchException(Exception):
    pass


class GameManager:
    BONUS_TIME_LIMIT = 20000  # In milliseconds
    MAX_TRAUMA = 1
    MIN_TRAUMA = 0

    def __init__(self, screen_size, fps_cap=60):
        self.FPS_CAP = fps_cap
        self.SCREEN_SIZE = screen_size

        self.dt = 0
        self.total_time = 0
        self.score = 0
        self.scenes = []
        self.current_scene = None
        self.status = GameStatus.PLAYING
        self.time_scale = 1
        self.use_perlin_noise = True

        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.DOUBLEBUF, vsync=True)

        # Set window title and icon
        pygame.display.set_caption("Space Invaders")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))

        self.screen_size = pygame.display.get_surface().get_size()
        self.screen_center = self.screen_size[0] / 2, self.screen_size[1] / 2

        pygame.font.init()
        self.font = pygame.font.Font("assets/fonts/Revamped.otf", 18)

        pygame.mixer.init()
        num_channels = 64
        pygame.mixer.set_num_channels(num_channels)

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
            self.dt = round(self.clock.tick(self.FPS_CAP) * self.time_scale)

            if not self.is_paused:
                # game.total_time = pygame.time.get_ticks() - game.start_time
                self.total_time += self.dt
                self.current_scene.total_time += self.dt

            camera = self.current_scene.camera

            factor = self.trauma ** 2
            camera.screen.fill((64 * factor, 32 * factor, 32 * factor))
            self.handle_events()

            if not self.is_paused:
                self.update(self.dt)
            self.draw()

            # camera.x = random.randint(-10, 10)
            # camera.y = random.randint(-10, 10)
            # camera.roll = random.randint(-100, 100) / 100

            # self.screen.blit(camera.transform(), (0, 0))
            camera.display(self.screen)
            pygame.display.flip()

        pygame.quit()

