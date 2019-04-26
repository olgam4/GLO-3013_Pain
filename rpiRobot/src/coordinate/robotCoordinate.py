from math import sqrt, atan, pi

from coordinate.orientation import Orientation


class RobotCoordinate:
    """Denotes a coordinates in the referential of the robot"""

    def __init__(self, x: float, y: float, orientation_change: Orientation) -> None:
        self._x = x
        self._y = y
        self._orientation_change = orientation_change

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def length(self) -> float:
        return sqrt(self._x ** 2 + self._y ** 2)

    @property
    def orientation_change(self) -> Orientation:
        return self._orientation_change

    @property
    def direction(self) -> Orientation:
        if self.y == 0 and self.x == 0:
            return Orientation(0)
        elif self.y == 0:
            return Orientation(pi / 2) if self.x > 0 else Orientation(-pi / 2)
        orientation = Orientation(atan(self.x / self.y))
        if self.y < 0:
            orientation = orientation + Orientation(pi)
        return orientation - self.orientation_change

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(RobotCoordinate.__name__, self.x, self.y, self.orientation_change)
