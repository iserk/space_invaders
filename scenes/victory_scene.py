import pygame

from scenes.scene import Scene
from game.game_manager import GameManager, GameStatus


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

