from typing import List

import cv2

from vision.domain.iCamera import ICamera
from vision.domain.iCameraFactory import ICameraFactory
from vision.infrastructure.cvCamera import CvCamera
from vision.infrastructure.cvVisionException import CameraDoesNotExistError
from vision.infrastructure.fileCamera import FileCamera


class CvCameraFactory(ICameraFactory):
    def __init__(self, max_camera_count: int = 10) -> None:
        self._max_camera_count = max_camera_count
        self._cameras: List[int] = [1337]
        self._find_all_camera()

    def get_cameras(self) -> List[int]:
        return self._cameras

    def create_camera(self, index: int) -> ICamera:
        if index not in self._cameras:
            raise CameraDoesNotExistError(index)
        if index == 1337:
            return FileCamera('./vision/infrastructure/2.jpg')
        return CvCamera(index)

    def _find_all_camera(self) -> None:
        index = 0

        while index < self._max_camera_count:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                cap.release()
                self._cameras.append(index)
            index += 1
