from math import pi
from unittest import TestCase

from coordinate.orientation import Orientation
from coordinate.robotCoordinate import RobotCoordinate


class TestRobotCoordinate(TestCase):
    def setUp(self) -> None:
        self.north = self.front = Orientation(0)
        self.northEast = self.frontRight = Orientation(pi / 4)
        self.east = self.right = Orientation(pi / 2)
        self.southEast = self.backRight = Orientation(3 * pi / 4)
        self.south = self.back = Orientation(pi)
        self.southWest = self.backLeft = Orientation(-3 * pi / 4)
        self.west = self.left = Orientation(-pi / 2)
        self.northWest = self.frontLeft = Orientation(-pi / 4)

    def test_given_movement_front_facing_north_then_direction_is_front(self) -> None:
        coordinate = RobotCoordinate(0, 1, self.north)

        self.assertEqual(self.front, coordinate.direction)

    def test_given_movement_right_facing_north_then_direction_is_right(self) -> None:
        coordinate = RobotCoordinate(1, 0, self.north)

        self.assertEqual(self.right, coordinate.direction)

    def test_given_movement_front_facing_east_then_direction_is_front(self) -> None:
        coordinate = RobotCoordinate(0, 1, self.east)

        self.assertEqual(self.front - self.east, coordinate.direction)

    def test_given_movement_left_facing_east_then_direction_is_left(self) -> None:
        coordinate = RobotCoordinate(-1, 0, self.east)

        self.assertEqual(self.left, coordinate.direction)

    def test_given_movement_backLeft_facing_west_then_direction_is_backLeft(self) -> None:
        coordinate = RobotCoordinate(-1, -1, self.west)

        self.assertEqual(self.backLeft - self.west, coordinate.direction)

    def test_given_movement_backRight_facing_west_then_direction_is_backRight(self) -> None:
        coordinate = RobotCoordinate(1, -1, self.west)

        self.assertEqual(self.backRight - self.west, coordinate.direction)

    def test_given_movement_frontRight_facing_west_then_direction_is_frontRight(self) -> None:
        coordinate = RobotCoordinate(1, 1, self.west)

        self.assertEqual(self.frontRight - self.west, coordinate.direction)

    def test_given_movement_frontLeft_facing_west_then_direction_is_frontLeft(self) -> None:
        coordinate = RobotCoordinate(-1, 1, self.west)

        self.assertEqual(self.frontLeft - self.west, coordinate.direction)
