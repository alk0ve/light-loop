# first must initialize pyglet resources
import pyglet
from pathlib import Path
pyglet.resource.path = [str(Path(__file__).resolve().parent / '../assets')]
pyglet.resource.reindex()

from typing import Final
WINDOW_WIDTH: Final = 1200
WINDOW_HEIGHT: Final = 800
window = pyglet.window.Window(resizable=False, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption="light loop")

# only now you can create sprites elsewhere
from levels import FIRST_LEVEL


def main():
    level = FIRST_LEVEL

    @window.event
    def on_draw():
        window.clear()
        level.draw()

    pyglet.app.run()


if "__main__" == __name__:
    main()
