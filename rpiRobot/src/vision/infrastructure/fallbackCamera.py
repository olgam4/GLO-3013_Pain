import numpy as np
from vision.domain.iCamera import ICamera
from vision.domain.image import Image


class FallbackCamera(ICamera):
    def __init__(self):
        self._width = 640
        self._height = 480

    def take_picture(self) -> Image:
        blank_image = np.zeros((self._height, self._width, 3), np.uint8)
        blank_image[:, 0:self._width // 6] = (255, 0, 0)
        blank_image[:, 1 * self._width // 6:2 * self._width // 6] = (255, 255, 0)
        blank_image[:, 2 * self._width // 6:3 * self._width // 6] = (0, 255, 0)
        blank_image[:, 3 * self._width // 6:4 * self._width // 6] = (0, 255, 255)
        blank_image[:, 4 * self._width // 6:5 * self._width // 6] = (0, 0, 255)
        blank_image[:, 5 * self._width // 6:self._width] = (255, 0, 255)
        return Image(blank_image)
