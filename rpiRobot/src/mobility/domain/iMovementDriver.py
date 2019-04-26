from abc import ABC, abstractmethod
from typing import overload

from cortex.domain.path.absoluteMovement import AbsoluteMovement
from cortex.domain.path.cameraMovement import CameraMovement
from mobility.domain.iDrivable import IDrivable


class IMovementDriver(ABC):
    @overload
    @abstractmethod
    def drive(self, movement: AbsoluteMovement, drivable: IDrivable) -> None: ...

    @overload
    @abstractmethod
    def drive(self, movement: CameraMovement, drivable: IDrivable) -> None: ...

    @abstractmethod
    def drive(self, movement, drivable: IDrivable) -> None:
        pass
