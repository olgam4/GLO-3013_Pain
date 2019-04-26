from abc import ABC, abstractmethod
from typing import List

from vision.domain.image import Image
from vision.domain.rectangle import Rectangle


class IObstacleFinder(ABC):
    @abstractmethod
    def find(self, image: Image) -> List[Rectangle]:
        pass
