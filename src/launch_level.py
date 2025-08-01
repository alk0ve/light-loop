# first must initialize pyglet resources
import pyglet
from pyglet.window import key
from pathlib import Path
pyglet.resource.path = [str(Path(__file__).resolve().parent / '../assets')]
pyglet.resource.reindex()

from typing import Final

WINDOW_WIDTH: Final = 1200
WINDOW_HEIGHT: Final = 800
window = pyglet.window.Window(resizable=False, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption="light loop")

# only now you can create sprites elsewhere
import levels
from enum import IntEnum, auto


class UIState(IntEnum):
    ANIMATING = auto()
    EDITING = auto()


def main():
    level = levels.SECOND_LEVEL
    pulse_batch = pyglet.graphics.Batch()
    front = set()
    pulses = None
    ui_state = UIState.EDITING

    @window.event
    def on_draw():
        window.clear()
        level.draw()
        if ui_state == UIState.ANIMATING:
            pulse_batch.draw()

    def update(delta_time):
        nonlocal pulses, front

        if ui_state == UIState.EDITING:
            # TODO UI
            return
        else:
            if len(front) == 0:
                animation_ends()
                print("done somehow")
                return

            if pulses.alive():
                pulses.update(delta_time)
            else:
                front = level.board.next_pulse_front(front)
                # print(f"new front: {front}")
                pulses = level.board.create_pulse_front(front, pulse_batch)

    def animation_ends():
        nonlocal front, pulses, ui_state
        level.board.reset()
        front = set()
        pulses = None
        ui_state = UIState.EDITING
        print("animation --> edit")

    @window.event
    def on_key_press(symbol, modifiers):
        nonlocal ui_state, pulses, front, level

        if symbol == key.SPACE:
            if ui_state == UIState.EDITING:
                print("edit --> animation")
                # start animating
                front = level.board.first_pulse_front()
                print(f"front = {front}")
                pulses = level.board.create_pulse_front(front, pulse_batch)
                ui_state = UIState.ANIMATING
                print("lets go")
            else:
                # stop animating
                animation_ends()

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


if "__main__" == __name__:
    main()
