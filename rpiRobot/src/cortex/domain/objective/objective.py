from cortex.domain.objective.color import Color
from cortex.domain.objective.shape import Shape


class Objective:
    def __init__(self, destination: int, shape: Shape, color: Color):
        self._destination = destination
        self._shape = shape
        self._color = color

    @property
    def destination(self) -> int:
        return self._destination

    @property
    def shape(self) -> Shape:
        return self._shape

    @property
    def color(self) -> Color:
        return self._color
