from cortex.domain.objective.color import Color
from cortex.domain.objective.item import Item
from cortex.domain.objective.shape import Shape
from polling.domain.address import Address


class Booth:
    def __init__(self, address: Address) -> None:
        self._address = address
        self._items = []

    @property
    def address(self) -> Address:
        return self._address

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def get_count(self) -> int:
        return len(self._items)

    def get_color(self) -> Color:
        colors = {
            Color.Red: 0,
            Color.Green: 0,
            Color.Blue: 0,
            Color.Yellow: 0
        }
        for item in self._items:
            colors[item.color] += 1
        popularity = max(colors[Color.Red], colors[Color.Green], colors[Color.Blue], colors[Color.Yellow])
        for color, votes in colors.items():
            if votes == popularity:
                return color

    def get_shape(self) -> Shape:
        shapes = {
            Shape.Triangle: 0,
            Shape.Square: 0,
            Shape.Pentagon: 0,
            Shape.Circle: 0
        }
        for item in self._items:
            shapes[item.shape] += 1
        popularity = max(shapes[Shape.Triangle], shapes[Shape.Square], shapes[Shape.Pentagon], shapes[Shape.Circle])
        for shape, votes in shapes.items():
            if votes == popularity:
                return shape

    def __repr__(self) -> str:
        return "{}(count:{},color:{},shape:{})".format(Booth.__name__, self.get_count(), self.get_color(),
                                                       self.get_shape())
