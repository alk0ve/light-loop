from enum import IntEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class NodeType(IntEnum):
    NO_NODE = auto()


class Node(object):
    """
    Represents a node on the board.
    Specifies an asset and its position on screen.
    """

    def __init__(self, asset_path: Path, x: int, y: int) -> None:
        self.asset = None  # TBD
        self.x = x
        self.y = y

    def draw(self) -> None:
        # TODO
        pass
