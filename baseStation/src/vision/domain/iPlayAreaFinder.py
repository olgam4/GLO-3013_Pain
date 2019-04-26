from abc import ABC, abstractmethod

from vision.domain.image import Image
from vision.domain.rectangle import Rectangle


class IPlayAreaFinder(ABC):
    @abstractmethod
    def find(self, image: Image) -> Rectangle:
        pass
