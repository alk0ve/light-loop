import pyglet
from abc import ABC, abstractmethod
from typing import Iterable, Callable
from collections import deque
from delayed_action import DelayedAction


class Animation(ABC):
    def __init__(self, end_action: DelayedAction = None) -> None:
        self.end_action = end_action

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

    def on_end(self) -> None:
        if self.end_action is not None:
            self.end_action.act()


class AnimationSequence(Animation):
    def __init__(self, animations: Iterable[Animation]) -> None:
        super().__init__()
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
            ended_animation = self.animations.popleft()
            ended_animation.on_end()

            if len(self.animations) > 0:
                self.animations[0].start(self.batch)

    def in_progress(self) -> bool:
        return len(self.animations) > 0
