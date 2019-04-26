from coordinate.cameraCoordinate import CameraCoordinate
from cortex.domain.objective.color import Color
from cortex.domain.objective.shape import Shape


class Item:
    def __init__(self, color: Color, shape: Shape, position: CameraCoordinate) -> None:
        self._color = color
        self._shape = shape
        self._position = position

    @property
    def color(self) -> Color:
        return self._color

    @property
    def shape(self) -> Shape:
        return self._shape

    @property
    def position(self) -> CameraCoordinate:
        return self._position

    def __repr__(self) -> str:
        return "{}({},{},{})".format(Item.__name__, self.color, self.shape, self.position)
