from enum import IntEnum, auto
from assets.asset_loader import load_image
import pyglet
from typing import Final


class NodeType(IntEnum):
    BLOCK = auto()
    BROADCAST = auto()
    BROADCAST_ONCE = auto()


class Node(object):
    """
    Represents a nodes on the board.
    Specifies an assets and its position on screen.
    """

    DEFAULT_SIZE: Final = 64

    def __init__(self,
                 asset_name: str | None,
                 x: int,
                 y: int,
                 width: int = DEFAULT_SIZE,
                 height: int = DEFAULT_SIZE) -> None:
        if asset_name is not None:
            self.sprite = pyglet.sprite.Sprite(load_image(asset_name), x=x, y=y)
            self.sprite.width = width
            self.sprite.height = height
        else:
            self.sprite = None
        self.x = x
        self.y = y

    def emit(self, neighbours: set[int], pulsing_neighbours: set[int]) -> set[int]:
        raise NotImplementedError

    def reset(self):
        pass


class BlockNode(Node):
    """
    Doesn't forward anything.
    """

    def __init__(self, x: int, y: int):
        super().__init__("nodes/Rock2_grass_shadow1.png", x, y)

    def emit(self, neighbours: set[int], pulsing_neighbours: set[int]) -> set[int]:
        return set()

    def reset(self):
        pass


class BroadcastOnceNode(Node):
    """
    Emit pulses to all the empty paths exactly once (don't reflect).
    Ignore incoming pulses.
    """

    def __init__(self, x: int, y: int):
        super().__init__("nodes/White_crystal2.png", x, y)
        self.emitted = False

    def emit(self, neighbours: set[int], pulsing_neighbours: set[int]) -> set[int]:
        if self.emitted:
            return set()
        self.emitted = True
        return neighbours - pulsing_neighbours

    def reset(self):
        self.emitted = False


class BroadcastNode(Node):
    """
    Emit pulses to all the empty paths.
    """

    def __init__(self, x: int, y: int):
        super().__init__("nodes/Dark_red_ crystal1.png", x, y)

    def emit(self, neighbours: set[int], pulsing_neighbours: set[int]) -> set[int]:
        return neighbours


def create_node(node_type: NodeType, x: int, y: int) -> Node:
    # print(f"create_node(node_type = {node_type}, x = {x}, y={y})")
    match node_type:
        case NodeType.BLOCK:
            return BlockNode(x, y)
        case NodeType.BROADCAST:
            return BroadcastNode(x, y)
        case NodeType.BROADCAST_ONCE:
            return BroadcastOnceNode(x, y)
        case _:
            raise ValueError(f"node_type {node_type} not supported")


def create_nodes(node_args: list[tuple[NodeType, int, int]]) -> list[Node]:
    return [create_node(*args) for args in node_args]
