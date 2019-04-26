from abc import ABC, abstractmethod

from vision.domain.image import Image


class ICamera(ABC):
    @abstractmethod
    def take_picture(self) -> Image:
        pass
