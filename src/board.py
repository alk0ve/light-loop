from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nodes.node import Node


class Board(object):
    """
    Represents the game board state throughout the game, including fog of war data.
    Consists of:
    - a list of Node objects
    - a list of paths between nodes (represented as a pair of indices into the nodes list)
    - a list of fog-of-war data (TBD)
    """

    def __init__(self, nodes: list[Node], paths: list[tuple[int, int]]) -> None:
        # TODO fog of war
        self.nodes = nodes
        self.paths = paths

    def draw(self):
        # TODO
        pass
