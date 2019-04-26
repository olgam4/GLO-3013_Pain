from json import dumps

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord


class Position:
    def __init__(self, coord: Coord, orientation: Angle):
        self._coord = coord
        self._orientation = orientation

    @property
    def coordinate(self) -> Coord:
        return self._coord

    @property
    def orientation(self) -> Angle:
        return self._orientation

    def serialize(self) -> str:
        return dumps({
            "x": self.coordinate.x,
            "y": self.coordinate.y,
            "orientation": self.orientation.radians
        })
