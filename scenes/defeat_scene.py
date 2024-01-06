import pygame
from game.game_manager import GameManager, GameStatus
from scenes.scene import Scene


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

