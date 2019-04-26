from collections import OrderedDict
from math import sqrt
from typing import List, Tuple

import cv2
import numpy as np

from coordinate.cameraCoordinate import CameraCoordinate
from vision.domain.iItemFinder import IItemFinder
from vision.domain.image import Image
from vision.domain.item.color import Color
from vision.domain.item.item import Item
from vision.domain.item.shape import Shape
from vision.domain.itemRelativePosition import ItemRelativePosition
from vision.domain.itemRelativePositions import ItemRelativePositions
from vision.infrastructure.openCvCamera import OpenCvCamera
from vision.infrastructure.openCvCameraCalibrationFactory import OpenCvCameraCalibrationFactory
from vision.infrastructure.openCvVisionError import CouldNotFindItemsError


class HSVItemFinder(IItemFinder):
    def __init__(self) -> None:
        self._items_relative_positions = None

        self.RED_MIN_1 = [0, 102, 127]
        self.RED_MAX_1 = [15, 255, 255]
        self.RED_MIN_2 = [170, 127, 127]
        self.RED_MAX_2 = [180, 255, 255]

        self.YELLOW_MIN = [19, 97, 204]
        self.YELLOW_MAX = [30, 255, 255]

        self.BLUE_MIN = [87, 204, 76]
        self.BLUE_MAX = [100, 255, 255]

        self.GREEN_MIN = [50, 204, 76]
        self.GREEN_MAX = [70, 100, 100]

    def find_items(self, image: Image) -> ItemRelativePositions:
        image.process(self._process)
        return self._items_relative_positions

    def _process(self, image: np.ndarray) -> None:
        image, zone_x, zone_y = HSVItemFinder._cut_zone(image)
        bin_image = HSVItemFinder._binarize_image(image)
        cv2.imshow('bin', bin_image)
        cv2.waitKey(1)

        _, contours, _ = cv2.findContours(bin_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [HSVItemFinder._approximate_contour(c) for c in contours]
        contours = [c for c in contours if HSVItemFinder._does_contour_fit_item(c)]
        if len(contours) == 0:
            raise CouldNotFindItemsError

        image_copy = image.copy()
        cv2.drawContours(image_copy, contours, -1, (0, 0, 255), 3)
        cv2.imshow('Contours', image_copy)
        cv2.waitKey(1)

        self._items_relative_positions = self._categorize_contours(image, zone_x, zone_y, contours)

    def _categorize_contours(self, zone: np.ndarray, zone_x: int, zone_y: int,
                             contours: List[np.ndarray]) -> ItemRelativePositions:
        image = cv2.cvtColor(zone, cv2.COLOR_BGR2HSV)

        item_relative_positions = []
        for contour in contours:
            try:
                color = self._compute_color(image, contour)
            except CouldNotFindItemsError:
                continue
            shape = HSVItemFinder._compute_shape(contour)
            item = Item(color, shape)
            camera_position = HSVItemFinder._compute_coordinate(contour, zone_x, zone_y)
            item_relative_positions.append(ItemRelativePosition(item, camera_position))

        return ItemRelativePositions(item_relative_positions)

    @staticmethod
    def _compute_shape(contour: np.ndarray) -> Shape:
        number_of_side = len(contour)
        if number_of_side == 3:
            return Shape.Triangle
        elif number_of_side == 4:
            return Shape.Square
        elif number_of_side == 5:
            return Shape.Pentagon
        else:
            return Shape.Circle

    def _compute_color(self, image: np.ndarray, contour: np.ndarray) -> Color:
        height, width, _ = image.shape
        mask = np.zeros([height, width], np.uint8)
        cv2.drawContours(mask, [contour], 0, 255, -1)
        h_mean, s_mean, v_mean, _ = cv2.mean(image, mask=mask)

        if self.YELLOW_MIN[0] < h_mean < self.YELLOW_MAX[0] and self.YELLOW_MIN[1] < s_mean < self.YELLOW_MAX[1] and \
           self.YELLOW_MIN[2] < v_mean < self.YELLOW_MAX[2]:
            return Color.Yellow
        elif self.GREEN_MIN[0] < h_mean < self.GREEN_MAX[0] and self.GREEN_MIN[1] < s_mean < self.GREEN_MAX[1] and \
             self.GREEN_MIN[2] < v_mean < self.GREEN_MAX[2]:
            return Color.Green
        elif self.BLUE_MIN[0] < h_mean < self.BLUE_MAX[0] and self.BLUE_MIN[1] < s_mean < self.BLUE_MAX[1] and \
             self.BLUE_MIN[2] < v_mean < self.BLUE_MAX[2]:
            return Color.Blue
        elif (self.RED_MIN_1[0] < h_mean < self.RED_MAX_1[0] and self.RED_MIN_1[1] < s_mean < self.RED_MAX_1[1] and \
              self.RED_MIN_1[2] < v_mean < self.RED_MAX_1[2]) or \
             (self.RED_MIN_2[0] < h_mean < self.RED_MAX_2[0] and self.RED_MIN_2[1] < s_mean < self.RED_MAX_2[1] and \
              self.RED_MIN_2[2] < v_mean < self.RED_MAX_2[2]):
            return Color.Red
        else:
            raise CouldNotFindItemsError

    @staticmethod
    def _compute_coordinate(contour: np.ndarray, zone_x: int, zone_y: int) -> CameraCoordinate:
        moments = cv2.moments(contour)
        x = int(moments['m10'] / moments['m00']) + zone_x
        y = int(moments['m01'] / moments['m00']) + zone_y
        return CameraCoordinate(x, y)

    @staticmethod
    def _cut_bottom_half(image: np.ndarray) -> np.ndarray:
        height, width, _ = image.shape
        return image[0: int(height / 2), 0: width, :]

    @staticmethod
    def _cut_zone(image: np.ndarray) -> Tuple[np.ndarray, int, int]:
        image = HSVItemFinder._cut_bottom_half(image)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, grey = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel = np.ones([5, 5], np.uint8)
        grey = cv2.morphologyEx(grey, cv2.MORPH_CLOSE, kernel)

        _, contours, _ = cv2.findContours(grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            raise CouldNotFindItemsError

        zone_contour = max(contours, key=cv2.contourArea)
        x, y, width, height = cv2.boundingRect(zone_contour)
        image = image[y:y + height, x:x + width, :]
        return image, x, y

    @staticmethod
    def _binarize_image(image: np.ndarray) -> np.ndarray:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(grey, threshold1=100, threshold2=200)
        kernel = np.ones([5, 5], np.uint8)
        canny = cv2.morphologyEx(canny, cv2.MORPH_DILATE, kernel)

        _, contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [HSVItemFinder._approximate_contour(c) for c in contours]
        contours = [c for c in contours if HSVItemFinder._does_contour_fit_item(c)]

        bin_image = np.zeros(grey.shape, np.uint8)
        for contour in contours:
            cv2.drawContours(bin_image, [contour], 0, 255, -1)
        return bin_image

    @staticmethod
    def _does_contour_fit_item(contour: np.ndarray) -> bool:
        contour = HSVItemFinder._approximate_contour(contour)
        _, _, width, height = cv2.boundingRect(contour)
        has_square_proportion = 0.85 <= width / float(height) <= 1.15

        is_big_enough = 300 < cv2.contourArea(contour) < 15000

        return has_square_proportion and is_big_enough

    @staticmethod
    def _approximate_contour(contour: np.ndarray) -> np.ndarray:
        epsilon = 0.05 * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)


def main():
    camera = OpenCvCamera(0)
    image = Image(cv2.imread('my_photo-4.jpg'))
    item_finder = HSVItemFinder()

    should_continue = True
    while should_continue:
        items = item_finder.find_items(image)

        for item in items.items:
            print('Color: {}, Shape: {}, Position: ({}, {})'.format(item.item.color, item.item.shape,
                                                                    item.camera_coordinate.x, item.camera_coordinate.y))

        key = cv2.waitKey(0)
        if key == ord('q'):
            should_continue = False

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
