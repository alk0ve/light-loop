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
    front = level.board.first_pulse_front()
    pulses = level.board.create_pulse_front(front, pulse_batch)
    print(f"starting front: {front}")

    @window.event
    def on_draw():
        window.clear()
        level.draw()
        pulse_batch.draw()

    def update(delta_time):
        nonlocal pulses, front

        if len(front) == 0:
            # print("front empty")
            return

        if pulses.alive():
            pulses.update(delta_time)
            print(f"update after {delta_time}")
        else:
            front = level.board.next_pulse_front(front)
            print(f"new front: {front}")
            pulses = level.board.create_pulse_front(front, pulse_batch)

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


if "__main__" == __name__:
    main()
