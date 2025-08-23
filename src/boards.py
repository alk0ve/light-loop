import pyglet
from nodes import Node
from typing import Final, Callable
from pulses import PulseFront
from loops import Loop
from delayed_action import DelayedAction

_PATH_COLOR: Final = (50, 82, 123)
_PATH_WIDTH: Final = 20.0

_INNER_PATH_COLOR: Final = (79, 115, 142)
_FRAME_THICKNESS: Final = 8


class Board(object):
    """
    Represents the game board state throughout the game, including fog of war data.
    Consists of:
    - a list of Node objects
    - a list of paths between nodes (represented as a pair of indices into the nodes list)
    - a list of fog-of-war data (TBD)
    """

    def __init__(self, nodes: list[Node], paths: set[tuple[int, int]]) -> None:
        # TODO fog of war
        self.nodes = nodes
        self.paths = paths  # used for rendering
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Group(order=0)
        self.background2 = pyglet.graphics.Group(order=1)
        self.foreground = pyglet.graphics.Group(order=2)
        self.shapes: list[pyglet.shapes.ShapeBase] = []

        # compute neighbour data
        self.neighbours = {}
        for i in range(len(paths)):
            self.neighbours[i] = set()
        for path in self.paths:
            i, j = path
            self.neighbours[i].add(j)
            self.neighbours[j].add(i)

        # mark the staring node
        circle = pyglet.shapes.Circle(x=nodes[0].x, y=nodes[0].y,
                                      radius=2 * Node.DEFAULT_SIZE // 3,
                                      color=_PATH_COLOR,
                                      batch=self.batch,
                                      group=self.background)
        self.shapes.append(circle)

        for node in self.nodes:
            if node.sprite is not None:
                node.sprite.batch = self.batch
                node.sprite.group = self.foreground
            # add a circle as background for each node
            circle = pyglet.shapes.Circle(x=node.x, y=node.y,
                                          radius=Node.DEFAULT_SIZE // 2,
                                          color=_PATH_COLOR,
                                          batch=self.batch,
                                          group=self.background)
            self.shapes.append(circle)
            inner_circle = pyglet.shapes.Circle(x=node.x, y=node.y,
                                                radius=(Node.DEFAULT_SIZE // 2) - _FRAME_THICKNESS,
                                                color=_INNER_PATH_COLOR,
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
                                      color=_PATH_COLOR,
                                      thickness=_PATH_WIDTH,
                                      batch=self.batch,
                                      group=self.background)
            self.shapes.append(line)
            inner_line = pyglet.shapes.Line(x=start_node.x,
                                            y=start_node.y,
                                            x2=end_node.x,
                                            y2=end_node.y,
                                            color=_INNER_PATH_COLOR,
                                            thickness=_PATH_WIDTH - _FRAME_THICKNESS,
                                            batch=self.batch,
                                            group=self.background2)
            self.shapes.append(inner_line)

    def draw(self):
        self.batch.draw()

    def reset_animation(self):
        for node in self.nodes:
            node.reset_animation()

    def first_pulse_front(self) -> set[tuple[int, int]]:
        front = self.nodes[0].emit(self.neighbours[0], set())
        return set([(0, f) for f in front])

    def next_pulse_front(self, last_front: set[tuple[int, int]]) -> set[tuple[int, int]]:
        next_front = set()

        # find all the pulsing neighbours for each neighbour
        pulsing_neighbours = {}
        for f in last_front:
            pulsing_neighbours[f[1]] = set()
        for f in last_front:
            pulsing_neighbours[f[1]].add(f[0])

        for neighbour, pulsing in pulsing_neighbours.items():
            front = self.nodes[neighbour].emit(self.neighbours[neighbour], pulsing)
            next_front.update([(neighbour, f) for f in front])

        return next_front

    def create_pulse_front(self, front: set[tuple[int, int]]) -> PulseFront:
        return PulseFront([(self.nodes[path[0]], self.nodes[path[1]]) for path in front])

    def create_loop(self, loop_edges: frozenset[tuple[int, int]], end_action: DelayedAction) -> Loop:
        return Loop([(self.nodes[path[0]], self.nodes[path[1]]) for path in loop_edges], end_action)
