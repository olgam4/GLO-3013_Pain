from typing import List

import cv2
import cv2.aruco as aruco
import numpy as np

from vision.domain.iObstacleFinder import IObstacleFinder
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle
from vision.infrastructure.cvImageDisplay import CvImageDisplay
from vision.infrastructure.cvVisionException import ObstaclesCouldNotBeFound


class CvObstacleFinder(IObstacleFinder):
    def __init__(self) -> None:
        self._aruco_dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self._obstacles_id = 0
        self._detection_parameter = aruco.DetectorParameters_create()
        self._obstacles: List[Rectangle] = []
        self._image_display = CvImageDisplay()

    def find(self, image: Image) -> List[Rectangle]:
        image.process(self._process)
        return self._obstacles

    def _process(self, image: np.ndarray) -> None:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, threshold = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self._image_display.display_debug_image('[CvObstacleFinder] threshold', threshold)

        corners, ids, _ = aruco.detectMarkers(threshold, self._aruco_dictionary, parameters=self._detection_parameter)
        self._image_display.display_debug_aruco_markers('[CvObstacleFinder] markers', image, corners, ids)

        self._obstacles.clear()
        if ids is not None:
            for i in range(ids.shape[0]):
                if ids[i] == self._obstacles_id:
                    min_x = np.min(corners[i][0, :, 0])
                    max_x = np.max(corners[i][0, :, 0])
                    min_y = np.min(corners[i][0, :, 1])
                    max_y = np.max(corners[i][0, :, 1])
                    self._obstacles.append(Rectangle(min_x, min_y, max_x - min_x, max_y - min_y))
        else:
            raise ObstaclesCouldNotBeFound
