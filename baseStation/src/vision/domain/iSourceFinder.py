from abc import ABC, abstractmethod
from typing import Tuple

from pathfinding.domain.angle import Angle
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle


class ISourceFinder(ABC):
    @abstractmethod
    def find(self, image: Image) -> Tuple[Rectangle, Angle]:
        pass
