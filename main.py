from game.game_manager import GameManager

from scenes.game_scene import GameScene
from scenes.defeat_scene import DefeatScene
from scenes.victory_scene import VictoryScene


SCREEN_SIZE = (1000, 800)
FPS_CAP = 60

if __name__ == '__main__':
    game = GameManager(SCREEN_SIZE, FPS_CAP)
    game.scenes.append(GameScene(game))
    game.scenes.append(DefeatScene(game))
    game.scenes.append(VictoryScene(game))
    game.switch_to_scene(game.scenes[0])

    game.run()