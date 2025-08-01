from enum import IntEnum, auto
from assets.asset_loader import load_image
import pyglet
from typing import Final


class NodeType(IntEnum):
    NO_NODE = auto()


class Node(object):
    """
    Represents a nodes on the board.
    Specifies an assets and its position on screen.
    """

    DEFAULT_HEIGHT: Final = 64
    DEFAULT_WIDTH: Final = 64

    def __init__(self,
                 asset_name: str,
                 x: int,
                 y: int,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT) -> None:
        self.sprite = pyglet.sprite.Sprite(load_image(asset_name), x=x, y=y)
        self.sprite.width = width
        self.sprite.height = height
        self.x = x
        self.y = y


class NoNode(Node):
    """
    An empty space, a placeholder for a past/future nodes.
    """

    def __init__(self, x: int, y: int):
        super().__init__("nodes/no-node.png", x, y)


####################################################################################
def create_node(node_type: NodeType, x: int, y: int) -> Node:
    # print(f"create_node(node_type = {node_type}, x = {x}, y={y})")
    match node_type:
        case NodeType.NO_NODE:
            return NoNode(x, y)
        case _:
            raise ValueError(f"node_type {node_type} not supported")


def create_nodes(node_types: list[NodeType], positions: list[tuple[int, int]]) -> list[Node]:
    assert len(node_types) == len(positions)
    return [create_node(node_types[i], *positions[i]) for i in range(len(node_types))]