from game_ui import GameUI
import levels


def main():
    # create a game window, and only then load levels (which involves creating pyglet sprites, and those sprites need
    # a pyglet window)
    game = GameUI()
    level = levels.second_level()
    game.load_level(level)
    game.start()


if "__main__" == __name__:
    main()
