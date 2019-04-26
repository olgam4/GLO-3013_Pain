from abc import ABC, abstractmethod

from pathfinding.domain.position import Position


class IApproachPositionFinder(ABC):
    @abstractmethod
    def calculate_from(self, position: Position) -> Position:
        pass
