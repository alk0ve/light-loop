from nodes import Node
import pyglet
from typing import Final

PATH_COLOR: Final = (50, 82, 123)
PATH_WIDTH: Final = 20.0

INNER_PATH_COLOR: Final = (79, 115, 142)
FRAME_THICKNESS: Final = 8


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
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Group(order=0)
        self.background2 = pyglet.graphics.Group(order=1)
        self.foreground = pyglet.graphics.Group(order=2)
        self.shapes: list[pyglet.shapes.ShapeBase] = []

        # place all the nodes in the same batch
        for node in self.nodes:
            if node.sprite is not None:
                node.sprite.batch = self.batch
                node.sprite.group = self.foreground
            # add a circle as background for each node
            circle = pyglet.shapes.Circle(x=node.x, y=node.y,
                                          radius=Node.DEFAULT_SIZE // 2,
                                          color=PATH_COLOR,
                                          batch=self.batch,
                                          group=self.background)
            self.shapes.append(circle)
            inner_circle = pyglet.shapes.Circle(x=node.x, y=node.y,
                                                radius=(Node.DEFAULT_SIZE // 2) - FRAME_THICKNESS,
                                                color=INNER_PATH_COLOR,
                                                batch=self.batch,
                                                group=self.background2)
            self.shapes.append(inner_circle)

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
                                      batch=self.batch,
                                      group=self.background)
            self.shapes.append(line)
            inner_line = pyglet.shapes.Line(x=start_node.x,
                                            y=start_node.y,
                                            x2=end_node.x,
                                            y2=end_node.y,
                                            color=INNER_PATH_COLOR,
                                            thickness=PATH_WIDTH - FRAME_THICKNESS,
                                            batch=self.batch,
                                            group=self.background2)
            self.shapes.append(inner_line)

    def draw(self):
        self.batch.draw()
