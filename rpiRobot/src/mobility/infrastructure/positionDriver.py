from typing import Union

from communication.service.positionService import PositionService
from coordinate.orientation import Orientation
from cortex.domain.path.absoluteMovement import AbsoluteMovement
from cortex.domain.path.cameraMovement import CameraMovement
from mobility.domain.angle import Angle
from mobility.domain.iDrivable import IDrivable
from mobility.domain.iMovementDriver import IMovementDriver
from mobility.infrastructure.directDriver import DirectDriver


class PositionDriver(IMovementDriver):
    close_position = 1.5
    angle_epsilon = 0.2

    def __init__(self, position_service: PositionService, direct_driver: DirectDriver):
        self._position_service = position_service
        self._direct_driver = direct_driver

    def drive(self, movement: Union[AbsoluteMovement, CameraMovement], drivable: IDrivable) -> None:
        if type(movement) == AbsoluteMovement:
            self._drive_absolute(movement, drivable)
        elif type(movement) == CameraMovement:
            self._drive_camera(movement, drivable)

    def _drive_absolute(self, movement: AbsoluteMovement, drivable: IDrivable) -> None:
        position = self._position_service.get_position()
        next_movement = AbsoluteMovement(movement.start, movement.stop)
        while next_movement.length > self.close_position or \
                not self._orientation_within_limits(position.orientation, movement.stop.orientation):
            self._direct_driver.drive(next_movement, drivable)
            position = self._position_service.get_position()
            next_movement = AbsoluteMovement(position, movement.stop)

    def _orientation_within_limits(self, actual: Orientation, referential: Orientation) -> bool:
        ref_angle = Angle(referential.radians)
        effective_ref_angle = Angle.to_effective(ref_angle)
        lower_limit = Angle(effective_ref_angle.radians - self.angle_epsilon)
        upper_limit = Angle(effective_ref_angle.radians + self.angle_epsilon)

        actual_angle = Angle(actual.radians)
        effective_actual_angle = Angle.to_effective(actual_angle)
        return lower_limit <= effective_actual_angle <= upper_limit

    def _drive_camera(self, movement: CameraMovement, drivable: IDrivable) -> None:
        self._direct_driver.drive(movement, drivable)
