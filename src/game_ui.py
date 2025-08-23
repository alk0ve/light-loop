from typing import Final
import pyglet
from pyglet.window import key
from pyglet.event import EVENT_HANDLE_STATE
from enum import IntEnum, auto
from levels import Level
from animations import AnimationSequence
from state_machines import UIStateMachine
from debug_print import DebugCategory, DebugPrintMixin
from game_states import GameState

_WINDOW_WIDTH: Final = 1200
_WINDOW_HEIGHT: Final = 800
_MANA_COLOR: Final = (255, 0, 255)
_TURN_COUNTER_COLOR: Final = (150, 150, 150)
_FRAME_RATE: Final = 60


class UIState(IntEnum):
    EMPTY = auto()
    ANIMATING = auto()
    EDITING = auto()


class GameUI(pyglet.window.Window, DebugPrintMixin):
    game_state: GameState | None
    animation: AnimationSequence | None

    def __init__(self) -> None:
        DebugPrintMixin.__init__(self, DebugCategory.UI)
        super().__init__(resizable=False, width=_WINDOW_WIDTH, height=_WINDOW_HEIGHT, caption="light loop")
        self.ui_batch = pyglet.graphics.Batch()
        self.game_state = None
        self.mana_label = pyglet.text.Label("0", color=_MANA_COLOR,
                                            font_size=25, x=10, y=10, batch=self.ui_batch)
        self.turn_label = pyglet.text.Label("0", color=_TURN_COUNTER_COLOR,
                                            font_size=25, x=180, y=10, batch=self.ui_batch)

        self.animation = None

        # define state machine callbacks
        def empty_draw() -> None:
            self.clear()
            self.ui_batch.draw()

        def regular_draw() -> None:
            self.clear()
            self.game_state.draw()
            self.ui_batch.draw()
            self.update_labels()

        def update_animating(delta_time: float) -> UIState:
            if self.animation is not None and self.animation.in_progress():
                self.animation.update(delta_time)
            else:
                return UIState.EDITING

        def exit_animating(_: UIState) -> None:
            self.game_state.reset_animation()
            self.animation = None

        def enter_animating(_: UIState) -> None:
            # start animating
            animations = []
            front = self.game_state.board.first_pulse_front()
            self.print(f"first front: {front}")

            while len(front) > 0:
                animations.append(self.game_state.board.create_pulse_front(front))
                loops = self.game_state.loop_detector.step(front)
                for loop in loops:
                    animations.append(self.game_state.board.create_loop(loop))

                front = self.game_state.board.next_pulse_front(front)
                self.print(f"front: {front}")

            self.animation = AnimationSequence(animations)
            self.animation.start(self.ui_batch)

        def handle_input_animating(symbol: int, modifiers: int) -> UIState:
            if symbol == key.SPACE:
                return UIState.EDITING

        def handle_input_editing(symbol: int, modifiers: int) -> UIState:
            if symbol == key.SPACE:
                return UIState.ANIMATING

        self.state_machine = UIStateMachine(initial_state=UIState.EMPTY,
                                            key_handlers={UIState.ANIMATING: handle_input_animating,
                                                          UIState.EDITING: handle_input_editing},
                                            update_handlers={UIState.ANIMATING: update_animating},
                                            draw_handlers={UIState.EMPTY: empty_draw,
                                                           '*': regular_draw},
                                            on_exit_handlers={UIState.ANIMATING: exit_animating},
                                            on_enter_handlers={UIState.ANIMATING: enter_animating})

    def load_level(self, level: Level) -> None:
        self.game_state = GameState(level)
        self.state_machine.transition(UIState.EDITING)

    def update_labels(self) -> None:
        self.mana_label.text = f"mana: {self.game_state.mana}"
        self.turn_label.text = f"turns left: {self.game_state.turns_left}"

    def update(self, delta_time: float) -> None:
        self.state_machine.update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.state_machine.handle_key(symbol, modifiers)

    def on_draw(self) -> EVENT_HANDLE_STATE:
        self.state_machine.draw()

    def start(self):
        pyglet.clock.schedule_interval(self.update, 1 / _FRAME_RATE)
        pyglet.app.run()
