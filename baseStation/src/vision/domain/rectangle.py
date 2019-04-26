from pathfinding.domain.coord import Coord


class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def get_center(self) -> Coord:
        return Coord(int(self._x + self.width / 2), int(self._y + self.height / 2))

    def is_square(self) -> bool:
        return 0.95 <= self.width_height_ratio <= 1.05

    @property
    def top_left_corner(self) -> Coord:
        return Coord(self._x, self._y)

    @property
    def bottom_right_corner(self) -> Coord:
        return Coord(self._x + self.width, self._y + self.height)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def width_height_ratio(self) -> float:
        return self.width / float(self.height)

    @property
    def area(self) -> int:
        return self.width * self.height
