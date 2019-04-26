from typing import List

from cortex.domain.path.cameraMovement import CameraMovement


class CameraPath:
    def __init__(self, movements: List[CameraMovement]) -> None:
        self._movements = movements

    @property
    def movements(self) -> List[CameraMovement]:
        return self._movements
