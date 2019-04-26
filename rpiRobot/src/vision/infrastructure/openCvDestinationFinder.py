import logging
from math import sqrt
from typing import Tuple

import cv2
import numpy as np

from coordinate.cameraCoordinate import CameraCoordinate
from vision.domain.iDestinationFinder import IDestinationFinder
from vision.domain.image import Image
from vision.domain.visionError import VisionError
from vision.infrastructure.openCvCamera import OpenCvCamera
from vision.infrastructure.openCvDebugDisplay import OpenCvDebugDisplay, VISION_DEBUG
from vision.infrastructure.openCvVisionError import CouldNotFindDestinationError


class OpenCvDestinationFinder(IDestinationFinder):
    def __init__(self) -> None:
        self._destination_to_find = 0
        self._destination_coordinate = CameraCoordinate(0, 0)
        self._debug_display = OpenCvDebugDisplay()

    def find_destination(self, image: Image, destination: int) -> CameraCoordinate:
        self._destination_to_find = destination
        image.process(self._process)
        return self._destination_coordinate

    def _process(self, image: np.ndarray) -> None:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grey = OpenCvDestinationFinder._cut_robot(grey)
        grey, zone_x, zone_y = self._cut_zone(grey)

        coordinate = self._find_destination_center(grey, self._destination_to_find)
        self._destination_coordinate = CameraCoordinate(coordinate.x + zone_x, coordinate.y + zone_y)

    def _cut_zone(self, image: np.ndarray) -> Tuple[np.ndarray, int, int]:
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        self._debug_display.display_debug_image('_cut_zone threshold', image)

        zone_x, zone_y, zone_width, zone_height = self._find_zone_contours(image)
        image = image[zone_y:zone_y + zone_height, zone_x:zone_x + zone_width]
        return image, zone_x, zone_y

    @staticmethod
    def _cut_robot(image: np.ndarray) -> np.ndarray:
        return image[0: 210, :]

    @staticmethod
    def _approximate_contour(contour: np.ndarray) -> np.ndarray:
        epsilon = 0.05 * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)

    def _find_zone_contours(self, image: np.ndarray) -> Tuple[int, int, int, int]:
        _, contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [OpenCvDestinationFinder._approximate_contour(c) for c in contours]
        contours = [c for c in contours if OpenCvDestinationFinder._is_contour_rectangle(c)]

        if len(contours) == 0:
            raise CouldNotFindDestinationError

        zone_contour = max(contours, key=cv2.contourArea)

        self._debug_display.display_debug_contours('_find_zone_contours', image, contours, [zone_contour])

        return cv2.boundingRect(zone_contour)

    @staticmethod
    def _is_contour_rectangle(contour: np.ndarray) -> bool:
        return len(contour) == 4

    def _find_destination_center(self, image: np.ndarray, destination: int) -> CameraCoordinate:
        zone_height, zone_width = image.shape

        coordinates = []
        for i in range(4):
            destination_width = int(zone_width / 4)
            destination_start = i * destination_width
            destination_end = destination_start + destination_width
            destination_roi = image[:, destination_start: destination_end]

            _, contours, _ = cv2.findContours(destination_roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = [c for c in contours if OpenCvDestinationFinder._does_contour_fit_destination_dot(c)]
            if len(contours) == 0:
                break

            destination_coordinate = CameraCoordinate(-1, -1)
            distance_to_center = float("inf")
            roi_center_x = destination_width / 2
            roi_center_y = zone_height / 2
            destination_found = False
            for contour in contours:
                try:
                    contour_center = OpenCvDestinationFinder._compute_contour_center(contour)
                    current_distance = sqrt((roi_center_x - contour_center.x) ** 2 + 
                                            (roi_center_y - contour_center.y) ** 2)
                    if current_distance < distance_to_center:
                        distance_to_center = current_distance
                        destination_coordinate = contour_center
                        destination_found = True
                except ValueError:
                    pass

            if self._debug_display.debug_active():
                image_copy = cv2.cvtColor(destination_roi, cv2.COLOR_GRAY2BGR)
                cv2.drawContours(image_copy, contours, -1, (0, 0, 255), 3)
                cv2.circle(image_copy, (destination_coordinate.x, destination_coordinate.y), 3, (0, 255, 0), 3)
                cv2.imshow('_find_destination_center {}'.format(i), image_copy)
                cv2.waitKey(1)

            if not destination_found:
                break

            coordinates.append(CameraCoordinate(destination_coordinate.x + destination_start, destination_coordinate.y))

        if len(coordinates) != 4:
            raise CouldNotFindDestinationError

        return coordinates[destination]

    @staticmethod
    def _does_contour_fit_destination_dot(contour: np.ndarray) -> bool:
        return 50 < cv2.contourArea(contour) < 250

    @staticmethod
    def _compute_contour_center(contour: np.ndarray) -> CameraCoordinate:
        moments = cv2.moments(contour)
        x = int(moments['m10'] / moments['m00'])
        y = int(moments['m01'] / moments['m00'])
        return CameraCoordinate(x, y)


def main():
    destination_finder = OpenCvDestinationFinder()
    camera = OpenCvCamera(2)
    logging.basicConfig(level=VISION_DEBUG)

    should_continue = True
    while should_continue:
        image = camera.take_picture()
        cv2.imshow('Capture', image.content)
        cv2.waitKey(1)
        for i in range(4):
            try:
                destination = destination_finder.find_destination(image, i)
                print('Destination {}, X: {}, Y: {}'.format(i, destination.x, destination.y))
            except VisionError as e:
                print(e.message)

        key = cv2.waitKey(20)
        if key == ord('q'):
            should_continue = False

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
