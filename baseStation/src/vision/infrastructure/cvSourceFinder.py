import logging
from math import pi
from typing import Tuple

import cv2
import numpy as np

from pathfinding.domain.angle import Angle
from vision.domain.iSourceFinder import ISourceFinder
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle
from vision.domain.visionError import VisionError
from vision.infrastructure.cvCamera import CvCamera
from vision.infrastructure.cvImageDisplay import CvImageDisplay
from vision.infrastructure.cvVisionException import SourceCouldNotBeFound


class CvSourceFinder(ISourceFinder):
    def __init__(self) -> None:
        self._source: Rectangle = None
        self._orientation: Angle = None
        self._image_display = CvImageDisplay()

    def find(self, image: Image) -> Tuple[Rectangle, Angle]:
        image.process(self._process)
        return self._source, self._orientation

    def _process(self, image: np.ndarray) -> None:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self._image_display.display_debug_image('[CvSourceFinder] grey', grey)

        _, threshold = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((5, 5), np.uint8)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        self._image_display.display_debug_image('[CvSourceFinder] threshold', threshold)

        contour_with_source = self._compute_biggest_contour(threshold, False)
        contour_without_source = self._compute_biggest_contour(threshold, True)
        source_contour = self._compute_source_contour(grey, contour_with_source, contour_without_source)

        self._image_display.display_debug_contours('[CvSourceFinder] contours', image,
                                                   [contour_with_source, contour_without_source], [source_contour])

        self._source = Rectangle(*cv2.boundingRect(source_contour))
        image_height, image_width, _ = image.shape
        self._compute_orientation(image_width, image_height)
        return None

    def _compute_source_contour(self, grey: np.ndarray, contour_with_source, contour_without_source):
        mask = np.zeros((grey.shape[0], grey.shape[1], 1), np.uint8)

        cv2.drawContours(mask, [contour_without_source], 0, 255, -1)
        cv2.drawContours(mask, [contour_with_source], 0, 0, -1)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)

        self._image_display.display_debug_image('[CvSourceFinder] source mask', mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [CvSourceFinder._approximate_contour(c) for c in contours]
        contours = [c for c in contours if CvSourceFinder._does_contour_fit_source(c)]
        if len(contours) == 0:
            raise SourceCouldNotBeFound

        source_mean_value = 256
        source_contour = None
        for contour in contours:
            mask = np.zeros(grey.shape, np.uint8)
            cv2.drawContours(mask, [contour], 0, 255, -1)

            current_mean_value, _, _, _ = cv2.mean(grey, mask=mask)
            if current_mean_value < source_mean_value:
                source_mean_value = current_mean_value
                source_contour = contour
        return source_contour

    def _compute_biggest_contour(self, image: np.ndarray, approximate):
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            raise SourceCouldNotBeFound

        biggest_contour = max(contours, key=cv2.contourArea)
        self._image_display.display_debug_contours('[CvSourceFinder] _compute_biggest_contour', image, contours,
                                                   [biggest_contour])

        if approximate:
            biggest_contour = CvSourceFinder._approximate_contour(biggest_contour)

        return biggest_contour

    @staticmethod
    def _approximate_contour(contour: np.ndarray) -> np.ndarray:
        epsilon = 0.05 * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)

    @staticmethod
    def _does_contour_fit_source(contour: np.ndarray) -> bool:
        is_rectangle = len(contour) == 4
        if is_rectangle:
            rectangle = Rectangle(*cv2.boundingRect(contour))
            # From experimentation, we know that the goal has an area of around 1650 pixels
            does_area_fit = 450 < rectangle.area < 2850
            return does_area_fit
        else:
            return False

    def _compute_orientation(self, image_width, image_height) -> None:
        goal_center = self._source.get_center()

        if self._source.width_height_ratio > 1.0:  # target is horizontal
            if goal_center.y > image_height / 2:  # target is on bottom
                self._orientation = Angle(pi)
            else:
                self._orientation = Angle(0)
        else:  # target is vertical
            if goal_center.x > image_width / 2:  # target is on the right
                self._orientation = Angle(pi / 2)
            else:
                self._orientation = Angle(3 * pi / 2)


def main():
    camera = CvCamera(0)
    source_finder = CvSourceFinder()
    logging.basicConfig(level=logging.DEBUG)

    while True:
        image = camera.take_picture()

        try:
            goal, orientation = source_finder.find(image)
            goal_center = goal.get_center()
            print('Goal found. x: {}, y: {}, Area: {}, orientation: {}'.format(goal_center.x, goal_center.y, goal.area,
                                                                               orientation))

        except VisionError as e:
            print(e.message)


if __name__ == '__main__':
    main()
