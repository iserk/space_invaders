from objects.camera import Camera
from objects.timer import Timer
from game.game_manager import GameManager

import pygame


class Scene:
    def __init__(self, game: GameManager):
        self.game = game
        self.objects = []
        self.total_time = 0
        self.bonus_time_left = 0
        self.camera = Camera(self.game.screen_size, 0, 0)
        self.is_input_enabled = False
        self.timers = []

    def activate(self):
        # print(f"Activated {self.__class__.__name__}")
        pass

    def add_object(self, obj):
        self.objects.append(obj)
        obj.scene = self

    def add_timer(self, interval, callback):
        print("Added timer with interval", interval, "and callback", callback)
        self.timers.append(Timer(interval, callback))

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
            screen.blit(pause_text, (self.game.screen_center[0] - pause_text.get_width() / 2, self.game.screen_center[1]))

    def draw(self):
        for obj in self.objects:
            obj.draw(self.camera)
        self.show_stats(self.camera.screen, self.game.clock)

    def update(self, dt):
        self.timers = [timer for timer in self.timers if timer.is_running]

        for timer in self.timers:
            timer.update(dt)

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
            self.add_object(obj)

    def __repr__(self):
        return f"{self.__class__.__name__}(game={self.game})"

