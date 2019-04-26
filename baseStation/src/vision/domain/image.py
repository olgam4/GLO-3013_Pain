from typing import Tuple, Callable, Optional

import cv2
import numpy as np

from vision.domain.rectangle import Rectangle


class Image:
    def __init__(self, content: np.ndarray) -> None:
        assert content.shape[2] == 3
        self._content = content

    @property
    def content(self) -> np.ndarray:
        return self._content.copy()

    @property
    def size(self) -> Tuple[int, int]:
        height, width, _ = self._content.shape
        return width, height

    def copy(self):  # -> Image
        return Image(self.content)

    def as_rgb(self) -> np.ndarray:
        return cv2.cvtColor(self.content, cv2.COLOR_BGR2RGB)

    def resize(self, width: int, height: int):
        return Image(cv2.resize(self.content, (width, height)))

    def crop(self, rectangle: Rectangle):
        return Image(self.content[rectangle.top_left_corner.y: rectangle.bottom_right_corner.y,
                     rectangle.top_left_corner.x: rectangle.bottom_right_corner.x, :])

    def process(self, process_callback: Callable[[np.ndarray], Optional[np.ndarray]]):  # -> Optional[Image]
        processed_content = process_callback(self.content)
        if processed_content is not None:
            return Image(processed_content)
