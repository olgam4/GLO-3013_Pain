from json import dumps
from typing import List

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord


class Table:
    def __init__(self, height: int, width: int, initial_data: int, exclusion_radius: float,
                 orientation: Angle, border: int) -> None:
        self._height = height
        self._width = width
        self._data: List[int] = []
        self._exclusion_radius = exclusion_radius
        self._orientation = orientation
        self._initialize_data(initial_data)
        self._border = border

    def _initialize_data(self, initial_value) -> None:
        self._data = [initial_value for _ in range(self._width * self._height)]

    @property
    def border(self) -> int:
        return self._border

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def exclusion_radius(self) -> float:
        return self._exclusion_radius

    @exclusion_radius.setter
    def exclusion_radius(self, value: float) -> None:
        self.exclusion_radius = value

    @property
    def data(self) -> List[float]:
        return [i for i in self._data]

    @property
    def orientation(self) -> Angle:
        return self._orientation

    @orientation.setter
    def orientation(self, value: Angle) -> None:
        self._orientation = value

    def __getitem__(self, cell: Coord) -> int:
        if cell.x >= self.width or cell.x < 0 or cell.y >= self.height or cell.y < 0:
            raise KeyError("cell is out of bounds")
        return self._data[cell.y * self._width + cell.x]

    def __setitem__(self, cell: Coord, value: int) -> None:
        if cell.x >= self.width or cell.x < 0 or cell.y >= self.height or cell.y < 0:
            raise KeyError("cell is out of bounds")

        self._data[cell.y * self._width + cell.x] = value

    def add_obstacle(self, obstacle: Coord) -> None:
        x_min = obstacle.x - self.exclusion_radius
        x_max = obstacle.x + self.exclusion_radius
        y_min = obstacle.y - self.exclusion_radius
        y_max = obstacle.y + self.exclusion_radius
        self._set_octogon_value_in_bounding_box(x_min, x_max, y_min, y_max, float("inf"))

    def clone(self):
        table = Table(self.height, self.width, 0, self.exclusion_radius, self.orientation, self.border)
        table._data = [i for i in self._data]
        return table

    def _set_octogon_value_in_bounding_box(self, x_min, x_max, y_min, y_max, value) -> None:
        first_value = self._exclusion_radius / 2
        removed = 1
        for row in range(y_min, y_max):
            for column in range(x_min, x_max):
                if x_min + first_value < column <= x_max - first_value:
                    cell = Coord(column, row)
                    try:
                        self[cell] = value
                    except KeyError:
                            pass
            if first_value != 0:
                removed += 1
            if row >= y_max - removed:
                first_value += 1
            else:
                first_value -= 1

    def __str__(self) -> str:
        table_str = ""
        for row in range(self.height):
            line = ""
            for column in range(self.width):
                value = str(self[Coord(column, row)])
                space = len(value)
                line += " " * (4 - space) + value
            table_str += line + "\n"
        return table_str

    def serialize(self) -> str:
        return dumps({
            "height": self.height,
            "width": self.width,
            "data": self.data,
            "orientation": self.orientation.radians
        })


if __name__ == "__main__":
    t = Table(50, 50, -1, 5, Angle(0), 10)
    print(t.serialize())
    print(t)
