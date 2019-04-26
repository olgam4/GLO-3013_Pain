import logging
from math import atan2, pi
from typing import Tuple

import cv2
import cv2.aruco as aruco
import numpy as np

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord
from vision.domain.iRobotFinder import IRobotFinder
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle
from vision.domain.visionError import VisionError
from vision.infrastructure.cvCamera import CvCamera
from vision.infrastructure.cvCameraCalibrationFactory import CvCameraCalibrationFactory
from vision.infrastructure.cvImageDisplay import CvImageDisplay
from vision.infrastructure.cvPlayAreaFinder import CvPlayAreaFinder
from vision.infrastructure.cvVisionException import RobotCouldNotBeFound


class CvRobotFinder(IRobotFinder):
    def __init__(self) -> None:
        self._aruco_dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self._top_left_id = 2
        self._top_right_id = 3
        self._bottom_left_id = 4
        self._bottom_right_id = 5
        self._ratio_distance_marker_size = 0.1
        self._detection_parameter = aruco.DetectorParameters_create()
        self._robot: Coord = None
        self._orientation: Angle = None
        self._image_display = CvImageDisplay()

    def find(self, image: Image) -> Tuple[Coord, Angle]:
        image.process(self._process)
        return self._robot, self._orientation

    def _process(self, image: np.ndarray) -> None:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, threshold = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self._image_display.display_debug_image('[CvRobotFinder] threshold', threshold)

        corners, ids, _ = aruco.detectMarkers(threshold, self._aruco_dictionary, parameters=self._detection_parameter)
        self._image_display.display_debug_aruco_markers('[CvRobotFinder] markers', image, corners, ids)
        if ids is None:
            raise RobotCouldNotBeFound

        robot_found = False
        i = 0
        while not robot_found and i < ids.shape[0]:
            if ids[i] == self._top_left_id:
                self._robot = self._interpolate_robot_position_from_corners(corners[i], 2, 1, 3)
                self._orientation = CvRobotFinder._compute_robot_orientation(corners[i])
                robot_found = True
            elif ids[i] == self._top_right_id:
                self._robot = self._interpolate_robot_position_from_corners(corners[i], 3, 0, 2)
                self._orientation = CvRobotFinder._compute_robot_orientation(corners[i])
                robot_found = True
            elif ids[i] == self._bottom_left_id:
                self._robot = self._interpolate_robot_position_from_corners(corners[i], 1, 0, 2)
                self._orientation = CvRobotFinder._compute_robot_orientation(corners[i])
                robot_found = True
            elif ids[i] == self._bottom_right_id:
                self._robot = self._interpolate_robot_position_from_corners(corners[i], 0, 3, 1)
                self._orientation = CvRobotFinder._compute_robot_orientation(corners[i])
                robot_found = True
            i += 1

        if not robot_found:
            raise RobotCouldNotBeFound

    def _interpolate_robot_position_from_corners(self, corners: np.ndarray, corner_to_adjust_index: int,
                                                 pred_corner_index: int, next_corner_index: int) -> Coord:
        x_to_adjust, y_to_adjust = CvRobotFinder._extract_corner_coordination(corners, corner_to_adjust_index)
        pred_x, pred_y = CvRobotFinder._extract_corner_coordination(corners, pred_corner_index)
        next_x, next_y = CvRobotFinder._extract_corner_coordination(corners, next_corner_index)

        x = x_to_adjust + self._ratio_distance_marker_size * (
                x_to_adjust - pred_x) + self._ratio_distance_marker_size * (x_to_adjust - next_x)
        y = y_to_adjust + self._ratio_distance_marker_size * (
                y_to_adjust - pred_y) + self._ratio_distance_marker_size * (y_to_adjust - next_y)

        return Coord(int(x), int(y))

    @staticmethod
    def _compute_marker_bounding_rectangle(corners: np.ndarray) -> Rectangle:
        min_x = np.min(corners[0, :, 0])
        max_x = np.max(corners[0, :, 0])
        min_y = np.min(corners[0, :, 1])
        max_y = np.max(corners[0, :, 1])
        return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

    @staticmethod
    def _compute_robot_orientation(corners: np.ndarray) -> Angle:
        return CvRobotFinder._compute_orientation_between_corners(corners, 3, 0)

    @staticmethod
    def _compute_orientation_between_corners(corners: np.ndarray, first_index: int, second_index: int) -> Angle:
        fourth_x, fourth_y = CvRobotFinder._extract_corner_coordination(corners, first_index)
        first_x, first_y = CvRobotFinder._extract_corner_coordination(corners, second_index)
        return Angle(atan2(fourth_y - first_y, fourth_x - first_x) - (pi / 2))

    @staticmethod
    def _extract_corner_coordination(corners: np.ndarray, corner_index: int) -> Tuple[int, int]:
        x = corners[0, corner_index, 0]
        y = corners[0, corner_index, 1]
        return x, y


def main():
    camera = CvCamera(2)
    robot_finder = CvRobotFinder()
    logging.basicConfig(level=logging.DEBUG)

    factory = CvCameraCalibrationFactory(CvPlayAreaFinder())
    calibration = factory.load_calibration_from_file(
        "/home/loup/Projects/glo-3013/doc/calib_table_4.npz", camera.take_picture())
    should_continue = True
    while should_continue:
        image = camera.take_picture()
        image = calibration.rectify_image(image)

        image_to_display = image.content
        try:
            robot_center, orientation = robot_finder.find(image)
            robot_center = calibration.convert_robot_pixel_to_real(robot_center)
            print('Robot found. x: {}, y: {}, orientation: {}'.format(robot_center.x, robot_center.y, orientation))
            cv2.circle(image_to_display, (robot_center.x, robot_center.y), 20, (0, 255, 0), -1)
        except VisionError as e:
            print(e.message)

        image_to_display = cv2.resize(image_to_display, (600, 600))
        cv2.imshow('Robot center', image_to_display)
        key = cv2.waitKey(0)
        if key == ord('q'):
            should_continue = False

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
