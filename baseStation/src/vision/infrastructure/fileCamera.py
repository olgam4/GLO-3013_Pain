import cv2

from vision.domain.iCamera import ICamera
from vision.domain.image import Image


class FileCamera(ICamera):
    def __init__(self, path: str):
        self._path = path

    def take_picture(self) -> Image:
        data = cv2.imread(self._path)
        return Image(data)
