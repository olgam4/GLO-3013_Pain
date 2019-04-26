from functools import total_ordering
from math import isclose


@total_ordering
class Distance:
    def __init__(self, centimeters: float):
        self._centimeters = centimeters

    @property
    def centimeters(self) -> float:
        return self._centimeters

    @classmethod
    def zero(cls):
        return Distance(0)

    def __eq__(self, other) -> bool:
        if not type(other) is Distance:
            return NotImplemented
        return isclose(self.centimeters, other.centimeters)

    def __lt__(self, other) -> bool:
        if not type(other) is Distance:
            return NotImplemented
        return self.centimeters < other.centimeters

    def __repr__(self) -> str:
        return "{}({})".format(Distance.__name__, self.centimeters)
