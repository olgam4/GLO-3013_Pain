from abc import ABC, abstractmethod

from coordinate.cameraCoordinate import CameraCoordinate
from vision.domain.image import Image


class IDestinationFinder(ABC):
    @abstractmethod
    def find_destination(self, image: Image, destination: int) -> CameraCoordinate:
        pass
