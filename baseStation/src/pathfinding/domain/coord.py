import math
from json import loads


class Coord:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def distance_from(self, other) -> float:
        if not isinstance(other, Coord):
            return NotImplemented
        return math.sqrt((self.y - other.y) ** 2 + (self.x - other.x) ** 2)

    @classmethod
    def deserialize(cls, data: str):
        deserialized = loads(data)
        return Coord(int(deserialized["x"]), int(deserialized["y"]))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Coord):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def to_centimeters(self):
        return Coord(int(self.x / 10), int(self.y / 10))

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)
