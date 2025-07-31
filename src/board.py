from nodes import Node
import pyglet


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
        self.nodes_batch = pyglet.graphics.Batch()

        # place all the nodes in the same batch
        for node in self.nodes:
            node.sprite.batch = self.nodes_batch

    def draw(self):
        self.nodes_batch.draw()
