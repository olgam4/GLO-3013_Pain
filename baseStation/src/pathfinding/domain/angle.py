from math import radians, degrees, isclose, pi


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

    def __add__(self, other):
        if not type(other) is Angle:
            return NotImplemented
        return Angle(self.radians + other.radians)

    def __sub__(self, other):
        if not type(other) is Angle:
            return NotImplemented
        return Angle(self.radians - other.radians)

    def __eq__(self, other) -> bool:
        if not type(other) is Angle:
            return NotImplemented
        return isclose(self.radians % (2 * pi), other.radians % (2 * pi), abs_tol=1e-9)

    def __repr__(self) -> str:
        return '{}({})'.format(Angle.__name__, self.degrees)
