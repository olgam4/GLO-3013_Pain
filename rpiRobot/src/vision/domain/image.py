from typing import Callable, Optional, Tuple

import numpy as np


class Image:
    def __init__(self, content: np.ndarray) -> None:
        assert content.shape[2] == 3
        self._content = content

    @property
    def content(self) -> np.ndarray:
        return self._content.copy()

    @property
    def width(self) -> int:
        return self._content.shape[1]

    @property
    def height(self) -> int:
        return self._content.shape[0]

    def process(self, process_callback: Callable[[np.ndarray], Optional[np.ndarray]]):  # -> Optional[Image]
        processed_content = process_callback(self.content)
        if processed_content is not None:
            return Image(processed_content)
