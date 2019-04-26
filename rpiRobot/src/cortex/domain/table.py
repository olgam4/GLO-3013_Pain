from json import loads
from typing import List

from coordinate.absoluteCoordinate import AbsoluteCoordinate
from coordinate.orientation import Orientation


class Table:
    def __init__(self, height: int, width: int, data: List[int], orientation: Orientation) -> None:
        self._height = height
        self._width = width
        self._data = data
        self._orientation = orientation

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def target_orientation(self) -> Orientation:
        return self._orientation

    def __getitem__(self, cell: AbsoluteCoordinate) -> int:
        if cell.x >= self.width or cell.x < 0 or cell.y >= self.height or cell.y < 0:
            raise KeyError("cell is out of bounds")
        return self._data[int(cell.y * self._width + cell.x)]

    def __setitem__(self, cell: AbsoluteCoordinate, value: int) -> None:
        if cell.x >= self.width or cell.x < 0 or cell.y >= self.height or cell.y < 0:
            raise KeyError("cell is out of bounds")
        self._data[int(cell.y * self._width + cell.x)] = value

    @classmethod
    def deserialize(cls, data_string: str):
        data = loads(data_string)
        return Table(data['height'], data['width'], data['data'], Orientation(data['orientation']))


if __name__ == "__main__":
    t = Table.deserialize('{"height": 3, "width": 3,'
                          ' "data": [2, 2, 2, 2, 2, 2, 2, 2, 2],'
                          ' "orientation": 0}')
    print(t)
