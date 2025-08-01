from nodes import Node
import pyglet
from typing import Final

PATH_COLOR: Final = (210, 180, 140)  # tan
PATH_WIDTH: Final = 20.0


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
        self.paths_batch = pyglet.graphics.Batch()
        self.shapes: list[pyglet.shapes.ShapeBase] = []

        # place all the nodes in the same batch
        for node in self.nodes:
            if node.sprite is not None:
                node.sprite.batch = self.nodes_batch
            # add a circle as background for each node
            circle = pyglet.shapes.Circle(x=node.x, y=node.y,
                                          radius=Node.DEFAULT_SIZE // 2,
                                          color=PATH_COLOR,
                                          batch=self.paths_batch)
            self.shapes.append(circle)

        # create path shapes
        for path in self.paths:
            start_node = self.nodes[path[0]]
            end_node = self.nodes[path[1]]
            line = pyglet.shapes.Line(x=start_node.x,
                                      y=start_node.y,
                                      x2=end_node.x,
                                      y2=end_node.y,
                                      color=PATH_COLOR,
                                      thickness=PATH_WIDTH,
                                      batch=self.paths_batch)
            self.shapes.append(line)

    def draw(self):
        self.paths_batch.draw()
        self.nodes_batch.draw()
