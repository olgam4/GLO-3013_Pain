from abc import abstractmethod, ABC
from typing import List

from coordinate.cameraCoordinate import CameraCoordinate
from cortex.domain.objective.item import Item
from cortex.domain.objective.objective import Objective


class IVisualCortex(ABC):
    @abstractmethod
    def find_objective(self) -> Objective:
        pass

    @abstractmethod
    def find_items(self) -> List[Item]:
        pass

    @abstractmethod
    def find_drop_position(self, objective: Objective) -> CameraCoordinate:
        pass
