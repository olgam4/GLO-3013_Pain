import logging
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
from vision.domain.visionError import VisionError
from vision.infrastructure.openCvCamera import OpenCvCamera
from vision.infrastructure.openCvDebugDisplay import OpenCvDebugDisplay, VISION_DEBUG
from vision.infrastructure.openCvVisionError import CouldNotFindItemsError


class OpenCvItemFinder(IItemFinder):
    def __init__(self) -> None:
        self._items_relative_positions = None
        self._debug_display = OpenCvDebugDisplay()

    def find_items(self, image: Image) -> ItemRelativePositions:
        image.process(self._process)
        return self._items_relative_positions

    def _process(self, image: np.ndarray) -> None:
        image = OpenCvItemFinder._grey_world_white_balance(image)
        self._debug_display.display_debug_image('White Balance', image)

        zone, zone_x, zone_y = self._cut_zone(image)
        self._debug_display.display_debug_image('Zone Image', zone)

        grey = cv2.cvtColor(zone, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(grey, 10, 200)
        kernel = np.ones((5, 5), np.uint8)
        canny = cv2.morphologyEx(canny, cv2.MORPH_DILATE, kernel)
        self._debug_display.display_debug_image('Zone Grey Canny', canny)

        item_contours = self._find_item_contours(canny, False, '_find_item_contours Canny')
        mask = np.zeros(canny.shape, np.uint8)
        for contour in item_contours:
            cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

        self._debug_display.display_debug_image('Item mask', mask)
        item_contours = self._find_item_contours(mask, True, '_find_item_contours Mask')

        hsv = cv2.cvtColor(zone, cv2.COLOR_BGR2HSV)
        hue = hsv[:, :, 0]
        self._debug_display.display_debug_image('Zone Hue', hue)
        self._items_relative_positions = self._categorize_contours(hue, zone_x, zone_y, item_contours)

    def _find_item_contours(self, image: np.ndarray, should_approximate: bool, debug_name: str) -> List[np.ndarray]:
        zone_area = image.shape[0] * image.shape[1]
        _, contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if should_approximate:
            contours = [OpenCvItemFinder._approximate_contour(c, 0.035) for c in contours]
        contours = [c for c in contours if OpenCvItemFinder._does_contour_fit_item(c, zone_area)]

        self._debug_display.display_debug_contours(debug_name, image, contours, [])

        if len(contours) == 0:
            raise CouldNotFindItemsError

        return contours

    @staticmethod
    def _does_contour_fit_item(contour: np.ndarray, zone_area: int) -> bool:
        _, _, width, height = cv2.boundingRect(contour)
        has_square_proportion = 0.85 <= width / float(height) <= 1.15

        is_big_enough = 500 < width * height < 0.25 * zone_area

        return has_square_proportion and is_big_enough

    def _categorize_contours(self, hue: np.ndarray, zone_x: int, zone_y: int,
                             contours: List[np.ndarray]) -> ItemRelativePositions:

        item_relative_positions = []
        for contour in contours:
            shape = OpenCvItemFinder._compute_shape(contour)
            color = self._compute_color(hue, contour)
            item = Item(color, shape)
            camera_position = OpenCvItemFinder._compute_coordinate(contour, zone_x, zone_y)
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

    @staticmethod
    def _compute_color(hue: np.ndarray, contour: np.ndarray) -> Color:
        mask = np.zeros(hue.shape, np.uint8)
        cv2.drawContours(mask, [contour], 0, 255, -1)
        histogram = cv2.calcHist([hue], [0], mask, [180], [0, 180])
        mode_hue = np.argmax(histogram)

        if 65 < mode_hue < 90:
            return Color.Green
        elif 90 < mode_hue < 115:
            return Color.Blue
        elif 14 < mode_hue < 37:
            return Color.Yellow
        else:
            return Color.Red

    @staticmethod
    def _compute_coordinate(contour: np.ndarray, zone_x: int, zone_y: int) -> CameraCoordinate:
        moments = cv2.moments(contour)
        try:
            x = int(moments['m10'] / moments['m00']) + zone_x
            y = int(moments['m01'] / moments['m00']) + zone_y
        except ZeroDivisionError:
            raise CouldNotFindItemsError
        return CameraCoordinate(x, y)

    def _cut_zone(self, image: np.ndarray) -> Tuple[np.ndarray, int, int]:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grey = OpenCvItemFinder._cut_robot(grey)

        _, threshold = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        self._debug_display.display_debug_image('_cut_zone threshold', threshold)

        zone_x, zone_y, zone_width, zone_height = self._find_zone_contours(threshold)
        image = image[zone_y:zone_y + zone_height, zone_x:zone_x + zone_width, :]
        return image, zone_x, zone_y

    @staticmethod
    def _cut_robot(image: np.ndarray) -> np.ndarray:
        return image[0: 210, :]

    def _find_zone_contours(self, image: np.ndarray) -> Tuple[int, int, int, int]:
        _, contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [OpenCvItemFinder._approximate_contour(c, 0.05) for c in contours]

        if len(contours) == 0:
            raise CouldNotFindItemsError

        zone_contour = max(contours, key=cv2.contourArea)

        self._debug_display.display_debug_contours('_find_zone_contours', image, contours, [zone_contour])

        return cv2.boundingRect(zone_contour)

    @staticmethod
    def _approximate_contour(contour: np.ndarray, arc_length_factor: float) -> np.ndarray:
        epsilon = arc_length_factor * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)

    @staticmethod
    def _grey_world_white_balance(image: np.ndarray) -> np.ndarray:
        result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)


def main():
    camera = OpenCvCamera(0)
    item_finder = OpenCvItemFinder()
    logging.basicConfig(level=VISION_DEBUG)

    should_continue = True
    while should_continue:
        image = camera.take_picture()
        cv2.imshow('Capture', image.content)
        cv2.waitKey(1)

        try:
            items = item_finder.find_items(image)
            detection = image.content.copy()
            for item in items.items:
                shape_text = '{}'.format(item.item.shape)
                color_text = '{}'.format(item.item.color)
                cX = item.camera_coordinate.x - 50
                cY = item.camera_coordinate.y
                detection = cv2.putText(detection, shape_text, (cX, cY),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                detection = cv2.putText(detection, color_text, (cX, cY + 15),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.imshow('Detection', detection)
            cv2.waitKey(1)

        except VisionError as e:
            print(e.message)

        key = cv2.waitKey(20)
        if key == ord('q'):
            should_continue = False

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
