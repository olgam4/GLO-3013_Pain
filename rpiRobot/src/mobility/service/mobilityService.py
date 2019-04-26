from threading import Lock
from typing import List, Union

from cortex.domain.path.absolutePath import AbsolutePath
from cortex.domain.path.cameraPath import CameraPath
from mobility.domain.iDrivable import IDrivable
from mobility.domain.operation.operation import Operation
from mobility.domain.iMovementDriver import IMovementDriver


class MobilityService:
    def __init__(self, drivable: IDrivable, movement_driver: IMovementDriver):
        self._drivable = drivable
        self._movement_driver = movement_driver
        self._driving = Lock()

    def drive(self, path: Union[AbsolutePath, CameraPath]) -> None:
        with self._driving:
            for movement in path.movements:
                self._movement_driver.drive(movement, self._drivable)

    def operate(self, operations: List[Operation]) -> None:
        with self._driving:
            for operation in operations:
                operation.execute(self._drivable)

    def brake(self) -> None:
        with self._driving:
            self._drivable.brake()
