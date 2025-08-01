import pyglet
from assets.asset_loader import load_image
from nodes import Node
from typing import Final


TRANSIT_TIME: Final = 1.0


class Pulse(object):
    x: float
    y: float
    vx: float
    vy: float
    t: float = 0

    def __init__(self, start_node: Node, end_node: Node, batch: pyglet.graphics.Batch):
        self.x = start_node.x
        self.y = start_node.y
        self.vx = (end_node.x - start_node.x) / TRANSIT_TIME
        self.vy = (end_node.y - start_node.y) / TRANSIT_TIME

        self.sprite = pyglet.sprite.Sprite(load_image("pulse/Icons_22.png"), x=self.x, y=self.y, batch=batch)

    def update(self, delta_time):
        self.t += delta_time
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.sprite.x = self.x
        self.sprite.y = self.y


class PulseFront(object):
    pulses: list[Pulse]

    t: float = 0

    def __init__(self, paths: list[tuple[Node, Node]], batch: pyglet.graphics.Batch):
        self.pulses = [Pulse(path[0], path[1], batch) for path in paths]

    def update(self, delta_time):
        self.t += delta_time

        for pulse in self.pulses:
            pulse.update(delta_time)

    def alive(self):
        return self.t < TRANSIT_TIME
