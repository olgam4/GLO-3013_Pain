from mobility.domain.angle import Angle
from mobility.domain.distance import Distance
from mobility.domain.iDrivable import IDrivable
from mobility.domain.operation.operation import Operation


class CarefulOperation(Operation):
    def __init__(self, angle: Angle, distance: Distance) -> None:
        self._angle = angle
        self._distance = distance

    def execute(self, drivable: IDrivable) -> None:
        drivable.careful(self._angle, self._distance)
