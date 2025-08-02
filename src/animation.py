from abc import ABC, abstractmethod


class Animation(ABC):
    @abstractmethod
    def update(self, delta_time) -> None:
        pass

    @abstractmethod
    def in_progress(self) -> bool:
        raise NotImplementedError

