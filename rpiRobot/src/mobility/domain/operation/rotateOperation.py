from mobility.domain.angle import Angle
from mobility.domain.iDrivable import IDrivable
from mobility.domain.operation.operation import Operation


class RotateOperation(Operation):
    def __init__(self, angle: Angle):
        self._angle = angle

    def execute(self, drivable: IDrivable) -> None:
        drivable.rotate(self._angle)
