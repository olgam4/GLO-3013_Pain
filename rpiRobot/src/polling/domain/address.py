from math import sqrt

from coordinate.cameraCoordinate import CameraCoordinate


class Address:
    minimal_distance = 1

    def __init__(self, coordinate: CameraCoordinate) -> None:
        self._coordinate = coordinate

    @property
    def coordinate(self) -> CameraCoordinate:
        return self._coordinate

    def __eq__(self, other) -> bool:
        if not type(other) is Address:
            return NotImplemented
        return sqrt((self.coordinate.x - other.coordinate.x) ** 2 + (
                    self.coordinate.y - other.coordinate.y) ** 2) < self.minimal_distance

    def __repr__(self) -> str:
        return "{}({})".format(Address.__name__, self.coordinate)
