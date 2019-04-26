from abc import ABC, abstractmethod

from mobility.domain.angle import Angle
from mobility.domain.distance import Distance


class IDrivable(ABC):
    @abstractmethod
    def translate(self, angle: Angle, distance: Distance) -> None:
        pass

    @abstractmethod
    def careful(self, angle: Angle, distance: Distance) -> None:
        pass

    @abstractmethod
    def rotate(self, angle: Angle) -> None:
        pass

    @abstractmethod
    def brake(self) -> None:
        pass
