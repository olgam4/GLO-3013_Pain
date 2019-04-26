import cv2

from vision.domain.iCamera import ICamera
from vision.domain.image import Image
from vision.infrastructure.cvImageDisplay import CvImageDisplay
from vision.infrastructure.cvVisionException import AcquisitionError, CameraDoesNotExistError


class CvCamera(ICamera):
    _buffer_size = 4

    def __init__(self, camera_id: int) -> None:
        self.image_display = CvImageDisplay()
        self._video_capture = cv2.VideoCapture(camera_id)
        if not self._video_capture.isOpened():
            raise CameraDoesNotExistError(camera_id)

    def __del__(self) -> None:
        self._video_capture.release()  # On Windows: Display "[ WARN:0] terminating async callback" in console

    def take_picture(self) -> Image:
        count = self._buffer_size
        while count > 0:
            self._video_capture.grab()
            count -= 1
        has_captured, cv_image = self._video_capture.read()

        if not has_captured:
            raise AcquisitionError()
        self.image_display.display_debug_image('[OpenCvCamera] take_picture', cv_image)
        return Image(cv_image)
