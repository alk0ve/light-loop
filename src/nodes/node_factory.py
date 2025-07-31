from typing import TYPE_CHECKING
from node import NodeType
from no_node import NoNode

if TYPE_CHECKING:
    from node import Node


def create_node(node_type: NodeType, x: int, y: int) -> Node:
    match node_type:
        case NodeType.NO_NODE:
            return NoNode(x, y)
        case _:
            raise ValueError(f"node_type {node_type} not supported")


def create_nodes(node_types: list[NodeType], positions: list[tuple[int, int]]) -> list[Node]:
    assert len(node_types) == len(positions)
    return [create_node(node_types[i], *positions[i]) for i in range(len(node_types))]
