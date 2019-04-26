from math import cos, sin

from numpy import array
from numpy.linalg import inv

from coordinate.absoluteCoordinate import AbsoluteCoordinate
from coordinate.orientation import Orientation
from coordinate.robotCoordinate import RobotCoordinate


class RobotCoordinateTransform:
    def __init__(self, robot_position: AbsoluteCoordinate) -> None:
        self._theta = -robot_position.orientation.radians
        transform_matrix_content = [[cos(self._theta), -sin(self._theta), robot_position.x],
                                    [-sin(self._theta), -cos(self._theta), robot_position.y],
                                    [0, 0, 1]]
        self._transform_matrix = array(transform_matrix_content)

    def from_absolute(self, coord: AbsoluteCoordinate) -> RobotCoordinate:
        homogeneous_coordinates = array([coord.x, coord.y, 1])
        transformed_coordinates = inv(self._transform_matrix) @ homogeneous_coordinates
        orientation = Orientation(self._theta + coord.orientation.radians)
        return RobotCoordinate(transformed_coordinates[0], transformed_coordinates[1], orientation)

    def from_robot(self, coord: RobotCoordinate) -> AbsoluteCoordinate:
        homogeneous_coordinates = array([coord.x, coord.y, 1])
        transformed_coordinates = self._transform_matrix @ homogeneous_coordinates
        orientation = Orientation(self._theta + coord.orientation_change.radians)
        return AbsoluteCoordinate(transformed_coordinates[0], transformed_coordinates[1], orientation)
