import logging

import cv2
import numpy as np

from vision.domain.iPlayAreaFinder import IPlayAreaFinder
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle
from vision.domain.visionError import VisionError
from vision.infrastructure.cvCamera import CvCamera
from vision.infrastructure.cvImageDisplay import CvImageDisplay
from vision.infrastructure.cvVisionException import PlayAreaCouldNotBeFound


class CvPlayAreaFinder(IPlayAreaFinder):
    def __init__(self) -> None:
        self._play_area: Rectangle = None
        self._image_display = CvImageDisplay()

    def find(self, image: Image) -> Rectangle:
        image.process(self._process)
        return self._play_area

    def _process(self, image: np.ndarray) -> None:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self._image_display.display_debug_image('[OpenCvPlayAreaFinder] grey', grey)

        _, threshold = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self._image_display.display_debug_image('[OpenCvPlayAreaFinder] threshold', threshold)

        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [CvPlayAreaFinder._approximate_contour(c) for c in contours]
        contours = [c for c in contours if CvPlayAreaFinder._does_contour_fit_area(c)]
        if len(contours) == 0:
            raise PlayAreaCouldNotBeFound

        contour_table = max(contours, key=cv2.contourArea)
        self._image_display.display_debug_contours('[OpenCvPlayAreaFinder] contours', image, contours, [contour_table])

        self._play_area = Rectangle(*cv2.boundingRect(contour_table))

    @staticmethod
    def _approximate_contour(contour: np.ndarray) -> np.ndarray:
        epsilon = 0.05 * cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, epsilon, True)

    @staticmethod
    def _does_contour_fit_area(contour: np.ndarray) -> bool:
        area = Rectangle(*cv2.boundingRect(contour))
        try:
            # The table is 231cm * 111cm, which gives it a width/height ratio of 2.08
            does_ratio_fit = 1.5 < area.width_height_ratio < 2.5

            return does_ratio_fit
        except ValueError:
            return False


def main():
    camera = CvCamera(2)
    play_area_finder = CvPlayAreaFinder()
    logging.basicConfig(level=logging.DEBUG)

    should_continue = True
    while should_continue:
        image = camera.take_picture()

        try:
            area = play_area_finder.find(image)
            print(
                'Area found. x: {}, y: {}, width: {}, height: {}'.format(area.top_left_corner.x, area.top_left_corner.y,
                                                                         area.width, area.height))
            crop_image = image.crop(area)
            cv2.imshow('[OpenCvPlayAreaFinder Main] CroppedResult', crop_image.content)
            key = cv2.waitKey(1)
            if key == ord('q'):
                should_continue = False

        except VisionError as e:
            print(e.message)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
