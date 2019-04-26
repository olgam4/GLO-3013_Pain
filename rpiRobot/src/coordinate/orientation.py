from functools import total_ordering
from math import degrees, pi, isclose


@total_ordering
class Orientation:
    def __init__(self, rads: float):
        self._radians = rads

    @property
    def radians(self) -> float:
        return self._radians

    @property
    def degrees(self) -> float:
        return degrees(self._radians)

    def __add__(self, other):
        if not type(other) is Orientation:
            return NotImplemented
        return Orientation(self.radians + other.radians)

    def __sub__(self, other):
        if not type(other) is Orientation:
            return NotImplemented
        return Orientation(self.radians - other.radians)

    def __eq__(self, other) -> bool:
        if not type(other) is Orientation:
            return NotImplemented
        return isclose(self.radians % (2 * pi), other.radians % (2 * pi), abs_tol=1e-9)

    def __lt__(self, other) -> bool:
        if not type(other) is Orientation:
            return NotImplemented
        return self.radians < other.radians

    def __repr__(self) -> str:
        return '{}({})'.format(Orientation.__name__, self.degrees)
