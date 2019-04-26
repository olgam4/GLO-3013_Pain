from abc import ABC, abstractmethod
from typing import List

from pathfinding.domain.coord import Coord
from pathfinding.domain.iPathfinder import IPathfinder


class IPathfinderFactory(ABC):
    @abstractmethod
    def create(self, obstacles: List[Coord]) -> IPathfinder:
        pass

    @property
    @abstractmethod
    def exclusion_radius(self) -> float:
        pass

    @exclusion_radius.setter
    @abstractmethod
    def exclusion_radius(self, value: float) -> None:
        pass
