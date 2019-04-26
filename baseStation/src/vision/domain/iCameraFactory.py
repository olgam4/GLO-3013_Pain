from abc import ABC, abstractmethod
from typing import List

from vision.domain.iCamera import ICamera


class ICameraFactory(ABC):
    @abstractmethod
    def get_cameras(self) -> List[int]:
        pass

    @abstractmethod
    def create_camera(self, index: int) -> ICamera:
        pass
