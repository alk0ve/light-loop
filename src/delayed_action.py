from abc import ABC, abstractmethod

from debug_print import DebugPrintMixin, DebugCategory


class DelayedAction(ABC, DebugPrintMixin):
    def __init__(self) -> None:
        DebugPrintMixin.__init__(self, DebugCategory.GAME)

    @abstractmethod
    def act(self) -> None:
        raise NotImplementedError
