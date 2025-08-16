from enum import Enum
from typing import TypeVar, Generic, Final, Optional
from debug_print import DebugPrintMixin, DebugCategory
from collections.abc import Callable

T = TypeVar('T', bound=Enum)
_WILDCARD: Final = '*'


class UIStateMachine(Generic[T], DebugPrintMixin):
    """
    You can use a '*' wildcard to specify they apply to all the states, but specific state/transition handlers always
    take precedence (for a T1-->T2 transition the order is: (T1, T2), (T1, *), (*, T2), (*, *)).
    Exactly one handler is called for each event.
    """

    def __init__(self,
                 initial_state: T,
                 key_handlers: dict[T | str, Callable[[int, int], T | None]] | None = None,
                 update_handlers: dict[T | str, Callable[[float], T | None]] | None = None,
                 draw_handlers: dict[T | str, Callable[[], None]] | None = None,
                 on_exit_handlers: dict[T | str, Callable[[T], None]] | None = None,
                 on_enter_handlers: dict[T | str, Callable[[T], None]] | None = None,
                 on_transition_handlers: dict[(T | str, T | str), Callable[[T, T], None]] | None = None):
        DebugPrintMixin.__init__(self, DebugCategory.STATE_MACHINE)
        self.state = initial_state
        self.key_handlers = key_handlers if key_handlers else dict()
        self.update_handlers = update_handlers if update_handlers else dict()
        self.draw_handlers = draw_handlers if draw_handlers else dict()
        self.on_exit_handlers = on_exit_handlers if on_exit_handlers else dict()
        self.on_enter_handlers = on_enter_handlers if on_enter_handlers else dict()
        self.on_transition_handlers = on_transition_handlers if on_transition_handlers else dict()

    def _get_handler(self, handlers: dict[T | str, Callable], state: T | str, name: str) -> Optional[Callable]:
        if state in handlers:
            return handlers[state]

        self.print(f"No specific {name} handler for state {state.name}")

        if _WILDCARD in handlers:
            return handlers[_WILDCARD]

        self.print(f"No generic {name} handler for state {state.name}")
        return None

    def transition(self, new_state: T) -> None:
        if new_state is None or self.state == new_state:
            self.print(f"Not transitioning from {self.state.name} to itself")
            return

        self.print(f"Transitioning from {self.state.name} to {new_state.name}")

        # on exit
        on_exit_handler = self._get_handler(self.on_exit_handlers, self.state, "exit")
        if on_exit_handler:
            on_exit_handler(self.state)

        # on transition
        # for a T1-->T2 transition the order is: (T1, T2), (T1, *), (*, T2), (*, *)
        for state_pair in ((self.state, new_state),
                           (self.state, _WILDCARD),
                           (_WILDCARD, new_state),
                           (_WILDCARD, _WILDCARD)):
            if state_pair in self.on_transition_handlers:
                self.print(f"Calling self.on_transition_handlers[{state_pair}]({self.state.name}, {new_state.name})")
                self.on_transition_handlers[state_pair](self.state, new_state)

        # on enter
        on_enter_handler = self._get_handler(self.on_enter_handlers, new_state, "enter")
        if on_enter_handler:
            on_enter_handler(new_state)

        self.state = new_state

    def handle_key(self, symbol: int, modifiers: int) -> None:
        self.print(f"Handling input for state {self.state.name} with symbol {symbol} and modifiers {modifiers}")

        handler = self._get_handler(self.key_handlers, self.state, "input")
        if not handler:
            return

        new_state = handler(symbol, modifiers)
        self.transition(new_state)

    def update(self, delta_time: float) -> None:
        self.print(f"Updating state {self.state.name} after {delta_time}s")

        handler = self._get_handler(self.update_handlers, self.state, "update")
        if not handler:
            return

        new_state = handler(delta_time)
        self.transition(new_state)

    def draw(self) -> None:
        self.print(f"Drawing in state {self.state.name}")

        handler = self._get_handler(self.draw_handlers, self.state, "draw")
        if not handler:
            return

        handler()
