from json import dumps
from math import atan2, sqrt

from coordinate.absoluteCoordinate import AbsoluteCoordinate
from coordinate.orientation import Orientation


class AbsoluteMovement:
    def __init__(self, start: AbsoluteCoordinate, stop: AbsoluteCoordinate):
        self._start = start
        self._stop = stop

    @property
    def start(self) -> AbsoluteCoordinate:
        return self._start

    @property
    def stop(self) -> AbsoluteCoordinate:
        return self._stop

    @stop.setter
    def stop(self, value: AbsoluteCoordinate) -> None:
        self._stop = value

    @property
    def direction(self) -> Orientation:
        angle = atan2(self.stop.x - self.start.x, self.stop.y - self.start.y)
        return Orientation(angle)

    @property
    def length(self) -> float:
        return sqrt((self.start.x - self.stop.x) ** 2 + (self.start.y - self.stop.y) ** 2)

    def serialize(self) -> str:
        return dumps({
            "start": self.start.serialize(),
            "stop": self.stop.serialize()
        })

    def __eq__(self, other) -> bool:
        if not type(other) is AbsoluteMovement:
            return NotImplemented
        return self.start == other.start and self.stop == other.stop

    def __repr__(self) -> str:
        return '{} -> {}'.format(self.start, self.stop)
