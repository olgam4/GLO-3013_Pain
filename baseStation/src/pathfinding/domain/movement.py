from json import loads

from pathfinding.domain.coord import Coord


class Movement:
    def __init__(self, start: Coord, end: Coord):
        self._start = start
        self._end = end

    @property
    def start(self) -> Coord:
        return self._start

    @property
    def end(self) -> Coord:
        return self._end

    @classmethod
    def deserialize(cls, data: str):
        deserialized = loads(data)
        return Movement(Coord.deserialize(deserialized["start"]), Coord.deserialize(deserialized["stop"]))
