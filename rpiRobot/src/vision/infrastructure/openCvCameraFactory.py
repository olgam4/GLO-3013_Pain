import cv2

from vision.domain.iCamera import ICamera
from vision.domain.iCameraFactory import ICameraFactory
from vision.infrastructure.fallbackCamera import FallbackCamera
from vision.infrastructure.openCvCamera import OpenCvCamera


class OpenCvCameraFactory(ICameraFactory):
    def __init__(self, max_camera_count: int = 10) -> None:
        self._max_camera_count = max_camera_count
        self._cameras = []
        self._find_all_camera()

    def create_camera(self) -> ICamera:
        if len(self._cameras) == 0:
            return FallbackCamera()
        index = self._cameras[0]
        return OpenCvCamera(index)

    def _find_all_camera(self) -> None:
        index = 0
        while index < self._max_camera_count:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                cap.release()
                self._cameras.append(index)
            index += 1
