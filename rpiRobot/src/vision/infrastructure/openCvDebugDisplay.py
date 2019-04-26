from logging import getLogger, DEBUG
from typing import List

import cv2
import numpy as np

logger = getLogger(__name__)
VISION_DEBUG = DEBUG + 5
Contour = np.ndarray


class OpenCvDebugDisplay:
    def __del__(self) -> None:
        cv2.destroyAllWindows()

    @staticmethod
    def debug_active() -> bool:
        return logger.getEffectiveLevel() == VISION_DEBUG

    def display_debug_image(self, window_name: str, image: np.ndarray) -> None:
        if OpenCvDebugDisplay.debug_active():
            cv2.imshow(window_name, image)
            cv2.waitKey(1)

    def display_debug_contours(self, window_name: str, image: np.ndarray, contours: List[Contour],
                               contours_of_interest: List[Contour]) -> None:
        if OpenCvDebugDisplay.debug_active():
            if len(image.shape) == 3:
                image_copy = image.copy()
            else:
                image_copy = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

            cv2.drawContours(image_copy, contours, -1, (0, 0, 255), 3)
            cv2.drawContours(image_copy, contours_of_interest, -1, (0, 255, 0), 3)
            cv2.imshow(window_name, image_copy)
            cv2.waitKey(1)
