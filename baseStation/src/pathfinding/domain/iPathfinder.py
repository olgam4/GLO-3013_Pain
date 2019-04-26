from abc import ABC, abstractmethod

from pathfinding.domain.position import Position
from pathfinding.domain.table import Table


class IPathfinder(ABC):
    @abstractmethod
    def pathable_to(self, position: Position) -> Table:
        pass
