from math import pi, sqrt
from typing import Tuple
from unittest import TestCase

from coordinate.absoluteCoordinate import AbsoluteCoordinate
from coordinate.orientation import Orientation
from coordinate.robotCoordinate import RobotCoordinate
from coordinate.robotCoordinateTransform import RobotCoordinateTransform


class TestRobotCoordinateTransform(TestCase):
    def assertRobotCoordIsCorrect(self, expected: Tuple[float, float], actual: RobotCoordinate) -> None:
        actual_coordinates = (actual.x, actual.y)
        for i in range(len(actual_coordinates)):
            self.assertAlmostEqual(expected[i], actual_coordinates[i])

    def test_given_no_orientation_when_converting_absolute_then_coordinate_is_correct(self) -> None:
        orientation = Orientation(0)
        start = AbsoluteCoordinate(5, 3, orientation)
        stop = AbsoluteCoordinate(7, 1, orientation)
        transform = RobotCoordinateTransform(start)

        actual_coordinate = transform.from_absolute(stop)

        self.assertRobotCoordIsCorrect((2, 2), actual_coordinate)

    def test_given_quarter_turn_right_when_converting_absolute_then_coordinate_is_correct(self) -> None:
        orientation = Orientation(pi / 2)
        start = AbsoluteCoordinate(5, 3, orientation)
        stop = AbsoluteCoordinate(7, 1, orientation)
        transform = RobotCoordinateTransform(start)

        actual_coordinate = transform.from_absolute(stop)

        self.assertRobotCoordIsCorrect((-2, 2), actual_coordinate)

    def test_given_quarter_turn_left_when_converting_absolute_then_coordinate_is_correct(self) -> None:
        orientation = Orientation(-pi / 2)
        start = AbsoluteCoordinate(5, 3, orientation)
        stop = AbsoluteCoordinate(7, 1, orientation)
        transform = RobotCoordinateTransform(start)

        actual_coordinate = transform.from_absolute(stop)

        self.assertRobotCoordIsCorrect((2, -2), actual_coordinate)

    def test_given_eight_turn_right_when_converting_absolute_then_coordinate_is_correct(self) -> None:
        orientation = Orientation(pi / 4)
        start = AbsoluteCoordinate(5, 3, orientation)
        stop = AbsoluteCoordinate(7, 1, orientation)
        transform = RobotCoordinateTransform(start)

        actual_coordinate = transform.from_absolute(stop)

        self.assertRobotCoordIsCorrect((0, sqrt(8)), actual_coordinate)

    def test_given_quarter_turn_right_from_north_when_converting_absolute_then_orientation_change_is_correct(
            self) -> None:
        orientation = Orientation(0)
        start = AbsoluteCoordinate(0, 0, orientation)
        orientation_change = Orientation(pi / 2)
        stop = AbsoluteCoordinate(0, 0, orientation + orientation_change)
        transform = RobotCoordinateTransform(start)

        actual_coordinate = transform.from_absolute(stop)

        self.assertEqual(orientation_change, actual_coordinate.orientation_change)

    def test_given_eight_turn_left_from_north_when_converting_absolute_then_orientation_change_is_correct(
            self) -> None:
        orientation = Orientation(0)
        start = AbsoluteCoordinate(0, 0, orientation)
        orientation_change = Orientation(-pi / 4)
        stop = AbsoluteCoordinate(0, 0, orientation + orientation_change)
        transform = RobotCoordinateTransform(start)

        actual_coordinate = transform.from_absolute(stop)

        self.assertEqual(orientation_change, actual_coordinate.orientation_change)

    def test_given_quarter_turn_right_from_south_when_converting_absolute_then_orientation_change_is_correct(
            self) -> None:
        orientation = Orientation(pi)
        start = AbsoluteCoordinate(0, 0, orientation)
        orientation_change = Orientation(pi / 2)
        stop = AbsoluteCoordinate(0, 0, orientation + orientation_change)
        transform = RobotCoordinateTransform(start)

        actual_coordinate = transform.from_absolute(stop)

        self.assertEqual(orientation_change, actual_coordinate.orientation_change)

    def test_given_eight_turn_left_from_south_when_converting_absolute_then_orientation_change_is_correct(
            self) -> None:
        orientation = Orientation(pi)
        start = AbsoluteCoordinate(0, 0, orientation)
        orientation_change = Orientation(-pi / 4)
        stop = AbsoluteCoordinate(0, 0, orientation + orientation_change)
        transform = RobotCoordinateTransform(start)

        actual_coordinate = transform.from_absolute(stop)

        self.assertEqual(orientation_change, actual_coordinate.orientation_change)
