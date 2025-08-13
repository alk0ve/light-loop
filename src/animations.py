import pyglet
from abc import ABC, abstractmethod
from typing import Iterable
from collections import deque


class Animation(ABC):
    @abstractmethod
    def start(self, batch: pyglet.graphics.Batch) -> None:
        """
        Add sprites to the batch here.
        """
        pass

    @abstractmethod
    def update(self, delta_time) -> None:
        pass

    @abstractmethod
    def in_progress(self) -> bool:
        raise NotImplementedError


class AnimationSequence(Animation):
    def __init__(self, animations: Iterable[Animation]) -> None:
        self.animations = deque(animations)
        self.batch = None

    def start(self, batch: pyglet.graphics.Batch) -> None:
        self.batch = batch

        if 0 == len(self.animations):
            return

        self.animations[0].start(batch)

    def update(self, delta_time) -> None:
        if 0 == len(self.animations):
            return

        self.animations[0].update(delta_time)

        if not self.animations[0].in_progress():
            self.animations.popleft()
            if len(self.animations) > 0:
                self.animations[0].start(self.batch)

    def in_progress(self) -> bool:
        return len(self.animations) > 0
