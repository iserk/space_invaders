from game.game_manager import GameManager

from scenes.game_scene import GameScene
from scenes.defeat_scene import DefeatScene
from scenes.victory_scene import VictoryScene

import settings

if __name__ == '__main__':
    game = GameManager(settings.SCREEN_SIZE, settings.FPS_CAP)
    game.scenes.append(GameScene(game))
    game.scenes.append(DefeatScene(game))
    game.scenes.append(VictoryScene(game))
    game.switch_to_scene(game.scenes[0])

    game.run()