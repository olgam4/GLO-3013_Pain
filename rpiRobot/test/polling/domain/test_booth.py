from unittest import TestCase

from coordinate.cameraCoordinate import CameraCoordinate
from cortex.domain.objective.color import Color
from cortex.domain.objective.item import Item
from cortex.domain.objective.shape import Shape
from polling.domain.address import Address
from polling.domain.booth import Booth


class TestBooth(TestCase):
    def setUp(self) -> None:
        self.triangle = Item(Color.Red, Shape.Triangle, CameraCoordinate(0, 0))
        self.red = self.triangle
        self.square = Item(Color.Green, Shape.Square, CameraCoordinate(0, 0))
        self.green = self.square
        self.pentagon = Item(Color.Blue, Shape.Pentagon, CameraCoordinate(0, 0))
        self.blue = self.pentagon
        self.circle = Item(Color.Yellow, Shape.Circle, CameraCoordinate(0, 0))
        self.yellow = self.circle

    def test_givenMajoritySquare_whenGettingShape_thenSquare(self) -> None:
        booth = Booth(Address(CameraCoordinate(1, 2)))
        for i in [self.square, self.square, self.square, self.square, self.triangle, self.pentagon]:
            booth.add_item(i)

        self.assertEqual(Shape.Square, booth.get_shape())

    def test_whenGettingCount_thenIsRight(self) -> None:
        booth = Booth(Address(CameraCoordinate(1, 2)))
        for i in [self.square, self.square, self.square, self.square, self.triangle, self.pentagon]:
            booth.add_item(i)

        self.assertEqual(6, booth.get_count())
