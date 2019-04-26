from math import cos, sin

from numpy import array
from numpy.linalg import inv

from coordinate.cameraCoordinate import CameraCoordinate
from coordinate.orientation import Orientation
from coordinate.robotCoordinate import RobotCoordinate


class CameraCoordinateTransform:
    def __init__(self, robot_position: CameraCoordinate) -> None:
        self._theta = 0
        transform_matrix_content = [[cos(self._theta), -sin(self._theta), robot_position.x],
                                    [-sin(self._theta), -cos(self._theta), robot_position.y],
                                    [0, 0, 1]]
        self._transform_matrix = array(transform_matrix_content)

    def from_camera(self, coord: CameraCoordinate) -> RobotCoordinate:
        homogeneous_coordinate = array([coord.x, coord.y, 1])
        transformed_coordinate = inv(self._transform_matrix) @ homogeneous_coordinate
        orientation = Orientation(self._theta)
        return RobotCoordinate(transformed_coordinate[0], transformed_coordinate[1], orientation)

    def from_robot(self, coord: RobotCoordinate) -> CameraCoordinate:
        homogeneous_coordinate = array([coord.x, coord.y, 1])
        transformed_coordinate = self._transform_matrix @ homogeneous_coordinate
        return CameraCoordinate(transformed_coordinate[0], transformed_coordinate[1])
