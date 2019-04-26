from logging import getLogger
from typing import List, Union

from coordinate.cameraCoordinateTransform import CameraCoordinateTransform
from coordinate.robotCoordinateTransform import RobotCoordinateTransform
from cortex.domain.path.absoluteMovement import AbsoluteMovement
from cortex.domain.path.cameraMovement import CameraMovement
from mobility.domain.angle import Angle
from mobility.domain.distance import Distance
from mobility.domain.iDrivable import IDrivable
from mobility.domain.operation.carefulOperation import CarefulOperation
from mobility.domain.operation.operation import Operation
from mobility.domain.operation.rotateOperation import RotateOperation
from mobility.domain.operation.translateOperation import TranslateOperation
from mobility.domain.iMovementDriver import IMovementDriver

logger = getLogger(__name__)


class DirectDriver(IMovementDriver):
    def drive(self, movement: Union[AbsoluteMovement, CameraMovement], drivable: IDrivable) -> None:
        operations = []
        if type(movement) == AbsoluteMovement:
            operations = self._calculate_absolute(movement)
        elif type(movement) == CameraMovement:
            operations = self._calculate_camera(movement)

        for operation in operations:
            operation.execute(drivable)

    @staticmethod
    def _calculate_absolute(movement: AbsoluteMovement) -> List[Operation]:
        robot_coordinate_transform = RobotCoordinateTransform(movement.start)
        robot_coordinate = robot_coordinate_transform.from_absolute(movement.stop)
        distance = Distance(robot_coordinate.length)
        rotation = Angle(robot_coordinate.orientation_change.radians)
        operations = []
        if rotation != Angle.zero():
            rotation = Angle.to_effective(rotation)
            operations.append(RotateOperation(rotation))
        if distance != Distance.zero():
            angle = Angle(robot_coordinate.direction.radians)
            angle = Angle.to_effective(angle)
            operations.append(TranslateOperation(angle, distance))
        return operations

    @staticmethod
    def _calculate_camera(movement: CameraMovement) -> List[Operation]:
        print("camera movement {}".format(movement))
        camera_coordinate_transform = CameraCoordinateTransform(movement.start)
        robot_coordinate = camera_coordinate_transform.from_camera(movement.stop)
        print("robot coordinate {}".format(robot_coordinate))
        distance = Distance(robot_coordinate.length)
        operations = []
        if distance != Distance.zero():
            angle = Angle(robot_coordinate.direction.radians)
            angle = Angle.to_effective(angle)
            operations.append(CarefulOperation(angle, distance))
        return operations
