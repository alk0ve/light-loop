from typing import Sequence, Final
import pyglet
from pyglet.window import key
from pyglet.event import EVENT_HANDLE_STATE
from enum import IntEnum, auto
from levels import Level
from loop import LoopDetector

_WINDOW_WIDTH: Final = 1200
_WINDOW_HEIGHT: Final = 800
_MANA_COLOR: Final = (255, 0, 255)
_TURN_COUNTER_COLOR: Final = (150, 150, 150)
_FRAME_RATE: Final = 60


class UIState(IntEnum):
    EMPTY = auto()
    ANIMATING = auto()
    EDITING = auto()


class GameUI(pyglet.window.Window):
    def __init__(self) -> None:
        super().__init__(resizable=False, width=_WINDOW_WIDTH, height=_WINDOW_HEIGHT, caption="light loop")
        self.level = None
        self.ui_batch = pyglet.graphics.Batch()
        self.mana = 0
        self.turns_left = 0
        self.mana_label = pyglet.text.Label("0", color=_MANA_COLOR,
                                            font_size=25, x=10, y=10, batch=self.ui_batch)
        self.turn_label = pyglet.text.Label("0", color=_TURN_COUNTER_COLOR,
                                            font_size=25, x=180, y=10, batch=self.ui_batch)

        self.front = set()
        self.pulses = None
        self.ui_state = UIState.EMPTY
        self.loop_detector = None

    def load_level(self, level: Level) -> None:
        self.level = level
        self.mana = level.starting_mana
        self.turns_left = level.turn_limit
        self.loop_detector = LoopDetector(len(level.board.nodes), level.board.neighbours)
        self.update_labels()
        self.ui_state = UIState.EDITING

    def update_labels(self) -> None:
        self.mana_label.text = f"mana: {self.mana}"
        self.turn_label.text = f"turns left: {self.turns_left}"

    def update(self, delta_time: float) -> None:
        match self.ui_state:
            case UIState.EDITING:
                # TODO UI
                return
            case UIState.ANIMATING:
                if len(self.front) == 0:
                    self.animation_ends()
                    return

                if self.pulses is not None and self.pulses.alive():
                    self.pulses.update(delta_time)
                else:
                    self.front = self.level.board.next_pulse_front(self.front)
                    # print(f"front: {self.front}")
                    loops = self.loop_detector.step(self.front)
                    self.pulses = self.level.board.create_pulse_front(self.front, self.ui_batch)

    def animation_ends(self) -> None:
        self.level.board.reset()  # check none?
        self.front = set()
        self.pulses = None
        self.ui_state = UIState.EDITING

    def on_key_press(self, symbol, modifiers) -> None:
        match self.ui_state:
            case UIState.EDITING:
                if symbol == key.SPACE:
                    # start animating
                    self.front = self.level.board.first_pulse_front()
                    # print(f"first front: {self.front}")
                    # TODO something with loops
                    loops = self.loop_detector.step(self.front)
                    self.pulses = self.level.board.create_pulse_front(self.front, self.ui_batch)
                    self.ui_state = UIState.ANIMATING
            case UIState.ANIMATING:
                if symbol == key.SPACE:
                    # stop animating
                    self.animation_ends()

    def on_draw(self) -> EVENT_HANDLE_STATE:
        self.clear()
        if self.ui_state != UIState.EMPTY:
            self.level.draw()
        self.ui_batch.draw()

    def start(self):
        pyglet.clock.schedule_interval(self.update, 1 / _FRAME_RATE)
        pyglet.app.run()
