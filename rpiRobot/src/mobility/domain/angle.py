from functools import total_ordering
from math import radians, degrees, isclose, pi


@total_ordering
class Angle:
    def __init__(self, rads: float):
        self._radians = rads

    @classmethod
    def from_degrees(cls, degs: float):
        return Angle(radians(degs))

    @property
    def radians(self) -> float:
        return self._radians

    @property
    def degrees(self) -> float:
        return degrees(self._radians)

    @classmethod
    def to_effective(cls, angle):
        if not type(angle) is Angle:
            return NotImplemented
        rads = angle.radians
        rads = rads % (2 * pi)
        if rads > pi:
            rads -= 2 * pi
        return Angle(rads)

    @classmethod
    def zero(cls):
        return Angle(0)

    def __eq__(self, other) -> bool:
        if not type(other) is Angle:
            return NotImplemented
        return isclose(self.radians % (2 * pi), other.radians % (2 * pi), abs_tol=1e-9)

    def __lt__(self, other) -> bool:
        if not type(other) is Angle:
            return NotImplemented
        return self.radians < other.radians

    def __repr__(self) -> str:
        return '{}({})'.format(Angle.__name__, self.degrees)
