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
from loop import LoopDetector


class UIState(IntEnum):
    ANIMATING = auto()
    EDITING = auto()


MANA_COLOR: Final = (255, 0, 255)
TURN_COUNTER_COLOR: Final = (150, 150, 150)


def main():
    level = levels.SECOND_LEVEL
    ui_batch = pyglet.graphics.Batch()
    front = set()
    pulses = None
    ui_state = UIState.EDITING

    mana = level.starting_mana
    turns = level.turn_limit
    mana_label = pyglet.text.Label(f"mana: {mana}", color=MANA_COLOR, font_size=25, x=10, y=10, batch=ui_batch)
    turn_label = pyglet.text.Label(f"turns left: {turns}", color=TURN_COUNTER_COLOR,
                                   font_size=25, x=180, y=10, batch=ui_batch)

    loop_detector = LoopDetector(len(level.board.nodes), level.board.neighbours)

    @window.event
    def on_draw():
        window.clear()
        level.draw()
        ui_batch.draw()

    def update(delta_time):
        nonlocal pulses, front

        if ui_state == UIState.EDITING:
            # TODO UI
            return
        else:
            if len(front) == 0:
                animation_ends()
                return

            if pulses is not None and pulses.alive():
                pulses.update(delta_time)
            else:
                front = level.board.next_pulse_front(front)
                print(f"front: {front}")
                loops = loop_detector.step(front)
                pulses = level.board.create_pulse_front(front, ui_batch)

    def animation_ends():
        nonlocal front, pulses, ui_state
        level.board.reset()
        front = set()
        pulses = None
        ui_state = UIState.EDITING

    @window.event
    def on_key_press(symbol, modifiers):
        nonlocal ui_state, pulses, front, level

        if symbol == key.SPACE:
            if ui_state == UIState.EDITING:
                # start animating
                front = level.board.first_pulse_front()
                print(f"first front: {front}")
                loops = loop_detector.step(front)
                pulses = level.board.create_pulse_front(front, ui_batch)
                ui_state = UIState.ANIMATING
            else:
                # stop animating
                animation_ends()

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


if "__main__" == __name__:
    main()
