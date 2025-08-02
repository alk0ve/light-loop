# first must initialize pyglet resources
import pyglet
from pathlib import Path
pyglet.resource.path = [str(Path(__file__).resolve().parent / '../assets')]
pyglet.resource.reindex()

from game_ui import GameUI
game = GameUI()

# only now you can create sprites elsewhere
import levels


def main():
    level = levels.second_level()
    game.load_level(level)
    game.start()


if "__main__" == __name__:
    main()
