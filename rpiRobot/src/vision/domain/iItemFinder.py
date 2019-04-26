from abc import ABC, abstractmethod

from vision.domain.image import Image
from vision.domain.itemRelativePositions import ItemRelativePositions


class IItemFinder(ABC):
    @abstractmethod
    def find_items(self, image: Image) -> ItemRelativePositions:
        pass
