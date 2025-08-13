import pyglet
from typing import Final, Iterable
from animations import Animation
from nodes import Node
from itertools import chain


class Loop(Animation):
    _LOOP_DURATION: Final = 1.0
    _LOOP_COLOR: Final = (255, 215, 0)
    _LOOP_WIDTH: Final = 10.0

    def __init__(self, loop_edges: Iterable[tuple[Node, Node]]) -> None:
        self.t = 0
        self.loop_edges = loop_edges
        self.shapes = []

    def start(self, batch: pyglet.graphics.Batch) -> None:
        for start_node, end_node in self.loop_edges:
            line = pyglet.shapes.Line(x=start_node.x,
                                      y=start_node.y,
                                      x2=end_node.x,
                                      y2=end_node.y,
                                      color=Loop._LOOP_COLOR,
                                      thickness=Loop._LOOP_WIDTH,
                                      batch=batch)
            self.shapes.append(line)

        # not all nodes appear as start nodes (our loops are weird)
        for node in set(chain.from_iterable(self.loop_edges)):
            circle = pyglet.shapes.Circle(x=node.x,
                                          y=node.y,
                                          radius=Loop._LOOP_WIDTH / 2,
                                          color=Loop._LOOP_COLOR,
                                          batch=batch)
            self.shapes.append(circle)

    def update(self, delta_time) -> None:
        self.t += delta_time
        # TODO loop fadeout

    def in_progress(self) -> bool:
        return self.t < Loop._LOOP_DURATION
