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
from pulse import PulseFront


def main():
    level = FIRST_LEVEL

    pulse_batch = pyglet.graphics.Batch()

    @window.event
    def on_draw():
        window.clear()
        level.draw()
        pulse_batch.draw()

    def update(delta_time):
        pass

    front = level.board.first_pulse_front()
    while len(front) > 0:
        print(front)
        front = level.board.next_pulse_front(last_front=front)


    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


if "__main__" == __name__:
    main()
