from logging import getLogger, DEBUG
from typing import List

import cv2
import cv2.aruco as aruco
import numpy as np

logger = getLogger(__name__)

Contour = np.ndarray


class CvImageDisplay:
    def __del__(self) -> None:
        cv2.destroyAllWindows()

    @staticmethod
    def debug_active() -> bool:
        return logger.getEffectiveLevel() <= DEBUG

    def display_debug_image(self, window_name: str, image: np.ndarray) -> None:
        if CvImageDisplay.debug_active():
            cv2.imshow(window_name, image)
            cv2.waitKey(1)

    def display_debug_contours(self, window_name: str, image: np.ndarray, contours: List[Contour],
                               contours_of_interest: List[Contour]) -> None:
        if CvImageDisplay.debug_active():
            if len(image.shape) == 3:
                image_copy = image.copy()
            else:
                image_copy = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(image_copy, contours, -1, (0, 0, 255), 3)
            cv2.drawContours(image_copy, contours_of_interest, -1, (0, 255, 0), 3)
            cv2.imshow(window_name, image_copy)
            cv2.waitKey(1)

    def display_debug_aruco_markers(self, window_name: str, image: np.ndarray, corners: List[np.ndarray],
                                    ids: List[np.ndarray]) -> None:
        if CvImageDisplay.debug_active():
            image_copy = image.copy()
            image_copy = aruco.drawDetectedMarkers(image_copy, corners, ids=ids, borderColor=(0, 0, 255))
            cv2.imshow(window_name, image_copy)
            cv2.waitKey(1)
