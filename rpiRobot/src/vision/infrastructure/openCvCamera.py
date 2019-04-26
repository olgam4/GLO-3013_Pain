import cv2

from vision.domain.iCamera import ICamera
from vision.domain.image import Image
from vision.infrastructure.openCvVisionError import CameraDoesNotExistError, AcquisitionError


class OpenCvCamera(ICamera):
    _buffer_size = 4

    def __init__(self, camera_id: int) -> None:
        self._video_capture = cv2.VideoCapture(camera_id)
        if not self._video_capture.isOpened():
            raise CameraDoesNotExistError(camera_id)
        self._video_capture.set(cv2.CAP_PROP_BUFFERSIZE, self._buffer_size)

    def __del__(self) -> None:
        self._video_capture.release()

    def take_picture(self) -> Image:
        count = self._buffer_size
        while count > 0:
            self._video_capture.grab()
            count -= 1
        has_captured, cv_image = self._video_capture.read()

        if not has_captured:
            raise AcquisitionError()
        return Image(cv_image)
