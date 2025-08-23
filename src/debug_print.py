from enum import auto, Enum
from typing import Final


class DebugCategory(Enum):
    STATE_MACHINE = auto()
    UI = auto()
    LOOPS = auto()
    GAME = auto()


_VERBOSE: Final = {DebugCategory.STATE_MACHINE: False,
                   DebugCategory.UI: False,
                   DebugCategory.LOOPS: False,
                   DebugCategory.GAME: False}

assert len(_VERBOSE) == len(DebugCategory), "Did you forget a category in the verbosity list?"


class DebugPrintMixin(object):
    """
    Inherit this, and call DebugPrintMixin.__init__(self, DebugCategory.<your category>), and then you can
    self.print(<whatever>)
    """
    def __init__(self, category: DebugCategory) -> None:
        self.category = category

    def print(self, *args, **kwargs) -> None:
        if not _VERBOSE[self.category]:
            return
        print(*args, **kwargs)
