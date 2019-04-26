from abc import ABC, abstractmethod
from typing import Tuple

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord
from vision.domain.image import Image


class IRobotFinder(ABC):
    @abstractmethod
    def find(self, image: Image) -> Tuple[Coord, Angle]:
        pass
