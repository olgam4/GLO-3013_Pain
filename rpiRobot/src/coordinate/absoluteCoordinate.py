from json import loads, dumps
from math import isclose

from coordinate.orientation import Orientation


class AbsoluteCoordinate:
    """Denotes a coordinate in the referential of the table"""

    def __init__(self, x_pos: float, y_pos: float, orientation: Orientation):
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._orientation = orientation

    @property
    def x(self) -> float:
        return self._x_pos

    @property
    def y(self) -> float:
        return self._y_pos

    @property
    def orientation(self) -> Orientation:
        return self._orientation

    @orientation.setter
    def orientation(self, value) -> None:
        self._orientation = value

    @classmethod
    def zero(cls):
        return AbsoluteCoordinate(0, 0, Orientation(0))

    def serialize(self):
        return dumps({
            "x": self.x,
            "y": self.y,
            "orientation": self.orientation.radians
        })

    @classmethod
    def deserialize(cls, data_string: str):
        data = loads(data_string)
        return AbsoluteCoordinate(data['x'], data['y'], Orientation(data['orientation']))

    def __eq__(self, other) -> bool:
        return isclose(self._x_pos, other.x, abs_tol=1e-9) and isclose(self._y_pos, other.y, abs_tol=1e-9) and \
               self._orientation == other.orientation

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(AbsoluteCoordinate.__name__, self.x, self.y, self.orientation)
