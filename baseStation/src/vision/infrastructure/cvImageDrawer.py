from typing import List

import cv2
import numpy as np

from vision.domain.iImageDrawer import IImageDrawer
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle


class CvImageDrawer(IImageDrawer):
    def __init__(self) -> None:
        self._color = (0, 0, 0)
        self._rectangle = Rectangle(0, 0, 0, 0)

    def draw_goal(self, image: Image, goal: Rectangle) -> Image:
        if goal is not None:
            self._color = (255, 0, 0)
            self._rectangle = goal
            image = image.process(self._draw_rectangle)
        return image

    def draw_obstacles(self, image: Image, obstacles: List[Rectangle]) -> Image:
        for obstacle in obstacles:
            self._color = (0, 0, 255)
            self._rectangle = obstacle
            image = image.process(self._draw_rectangle)
        return image

    def draw_source(self, image: Image, source: Rectangle) -> Image:
        if source is not None:
            self._color = (0, 255, 0)
            self._rectangle = source
            image = image.process(self._draw_rectangle)
        return image

    def _draw_rectangle(self, image: np.ndarray) -> np.ndarray:
        top_left_corner = (self._rectangle.top_left_corner.x, self._rectangle.top_left_corner.y)
        bottom_right_corner = (self._rectangle.bottom_right_corner.x, self._rectangle.bottom_right_corner.y)
        cv2.rectangle(image, top_left_corner, bottom_right_corner, self._color, 3)
        return image
