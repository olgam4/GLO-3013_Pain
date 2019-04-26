import logging
from math import pi
from typing import Tuple, List

import cv2
import numpy as np

from pathfinding.domain.angle import Angle
from vision.domain.iGoalFinder import IGoalFinder
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle
from vision.domain.visionError import VisionError
from vision.infrastructure.cvCamera import CvCamera
from vision.infrastructure.cvImageDisplay import CvImageDisplay
from vision.infrastructure.cvPlayAreaFinder import CvPlayAreaFinder
from vision.infrastructure.cvVisionException import GoalCouldNotBeFound


class CvGoalFinder(IGoalFinder):
    def __init__(self) -> None:
        self._goal: Rectangle = None
        self._orientation: Angle = None
        self._play_area_finder = CvPlayAreaFinder()
        self._image_display = CvImageDisplay()

    def find(self, image: Image) -> Tuple[Rectangle, Angle]:
        play_area = self._play_area_finder.find(image)
        image.crop(play_area).process(self._process)
        self._goal = Rectangle(self._goal.top_left_corner.x + play_area.top_left_corner.x,
                               self._goal.top_left_corner.y + play_area.top_left_corner.y, self._goal.width,
                               self._goal.height)
        return self._goal, self._orientation

    def _process(self, image: np.ndarray) -> None:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self._image_display.display_debug_image('[CvGoalFinder] grey', grey)

        canny = cv2.Canny(grey, 100, 200)
        self._image_display.display_debug_image('[CvGoalFinder] canny', canny)

        contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [CvGoalFinder._approximate_contour(c) for c in contours]
        contours = [c for c in contours if CvGoalFinder._does_contour_fit_goal(c)]
        if len(contours) == 0:
            raise GoalCouldNotBeFound

        goal_contour = CvGoalFinder._get_brightest_area(grey, contours)

        self._goal = Rectangle(*cv2.boundingRect(goal_contour))
        image_height, image_width, _ = image.shape
        self._compute_orientation(image_width, image_height)
        self._image_display.display_debug_contours('[CvGoalFinder] goal_contour', image, contours, [goal_contour])

    @staticmethod
    def _does_contour_fit_goal(contour: np.ndarray) -> bool:
        is_contour_rectangle = len(contour) == 4
        rectangle = Rectangle(*cv2.boundingRect(contour))

        # goal area is 27cm * 7.5cm, which gives a width/height ratio of 3.6 or 0.27
        ratio = rectangle.width_height_ratio
        does_ratio_fit = 2.6 < ratio < 4.6 or 2.6 < (1.0 / ratio) < 4.6

        # From experimentation, we know that the goal has an area of around 1650 pixels
        does_area_fit = 650 < rectangle.area < 2650

        return is_contour_rectangle and does_ratio_fit and does_area_fit

    @staticmethod
    def _approximate_contour(contour: np.ndarray) -> np.ndarray:
        epsilon = 0.05 * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)

    @staticmethod
    def _get_brightest_area(grey: np.ndarray, contours: List[np.ndarray]) -> np.ndarray:
        highest_mean_value = -1
        brightest_area_contour = None

        for contour in contours:
            mask = np.zeros(grey.shape, np.uint8)
            cv2.drawContours(mask, [contour], 0, 255, -1)

            current_mean_value, _, _, _ = cv2.mean(grey, mask=mask)

            if current_mean_value > highest_mean_value:
                highest_mean_value = current_mean_value
                brightest_area_contour = contour

        return brightest_area_contour

    def _compute_orientation(self, image_width, image_height) -> None:
        goal_center = self._goal.get_center()

        if self._goal.width_height_ratio > 1.0:  # target is horizontal
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
    camera = CvCamera(1)
    goal_finder = CvGoalFinder()
    logging.basicConfig(level=logging.DEBUG)

    while True:
        image = camera.take_picture()

        try:
            goal, orientation = goal_finder.find(image)
            goal_center = goal.get_center()
            print('Goal found. x: {}, y: {}, Area: {}, orientation: {}'.format(goal_center.x, goal_center.y, goal.area,
                                                                               orientation))

        except VisionError as e:
            print(e.message)


if __name__ == '__main__':
    main()
