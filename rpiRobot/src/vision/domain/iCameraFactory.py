from abc import ABC, abstractmethod

from vision.domain.iCamera import ICamera


class ICameraFactory(ABC):
    @abstractmethod
    def create_camera(self) -> ICamera:
        pass
