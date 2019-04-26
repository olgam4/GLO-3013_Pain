from vision.domain.item.color import Color
from vision.domain.item.shape import Shape


class Item:
    def __init__(self, color: Color, shape: Shape):
        self._color = color
        self._shape = shape

    @property
    def color(self) -> Color:
        return self._color

    @property
    def shape(self) -> Shape:
        return self._shape
