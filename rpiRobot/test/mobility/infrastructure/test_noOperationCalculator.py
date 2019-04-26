from math import pi
from unittest import TestCase
from unittest.mock import Mock, patch, call

from coordinate.absoluteCoordinate import AbsoluteCoordinate
from coordinate.orientation import Orientation
from cortex.domain.path.absoluteMovement import AbsoluteMovement
from mobility.domain.angle import Angle
from mobility.domain.distance import Distance
from mobility.domain.operation.rotateOperation import RotateOperation
from mobility.domain.operation.translateOperation import TranslateOperation
from mobility.infrastructure.directDriver import DirectDriver


class TestNoOperationCalculator(TestCase):
    def setUp(self) -> None:
        rct_patcher = patch('mobility.infrastructure.directDriver.RobotCoordinateTransform')
        self.RobotCoordinateTransform = rct_patcher.start()
        self.addCleanup(rct_patcher.stop)

        self.robot_coordinate_transform = Mock()
        self.RobotCoordinateTransform.return_value = self.robot_coordinate_transform

        self.robot_coordinate = Mock()
        self.robot_coordinate.length = 0
        self.robot_coordinate.orientation_change = Orientation(0)
        self.robot_coordinate.direction = Orientation(0)
        self.robot_coordinate_transform.from_absolute.return_value = self.robot_coordinate

        self.drivable = Mock()

        self.direct_driver = DirectDriver()

    def test_givenMovement_whenCalculating_thenStartIsUsedToInstantiateRCT(self) -> None:
        start = AbsoluteCoordinate(0, 0, Orientation(0))
        stop = AbsoluteCoordinate(0, 0, Orientation(0))
        movement = AbsoluteMovement(start, stop)

        self.direct_driver.drive(movement, self.drivable)

        self.RobotCoordinateTransform.assert_called_with(start)

    def test_givenMovement_whenCalculating_thenStopIsUsedToCalculateRobotCoordinate(self) -> None:
        start = AbsoluteCoordinate(0, 0, Orientation(0))
        stop = AbsoluteCoordinate(0, 0, Orientation(0))
        movement = AbsoluteMovement(start, stop)

        self.direct_driver.drive(movement, self.drivable)

        self.robot_coordinate_transform.from_absolute.assert_called_with(stop)

    def test_givenZeroDistanceMovement_whenCalculating_thenRotateOperationReturned(self) -> None:
        start = AbsoluteCoordinate(0, 0, Orientation(0))
        stop = AbsoluteCoordinate(0, 0, Orientation(pi))
        self.robot_coordinate.orientation_change = Angle(pi)
        movement = AbsoluteMovement(start, stop)

        self.direct_driver.drive(movement, self.drivable)

        expected_calls = [call.rotate(Angle(pi))]
        actual_calls = self.drivable.method_calls
        self.assertListEqual(expected_calls, actual_calls)

    def test_givenNonZeroDistanceMovement_whenCalculating_thenTranslateOperationReturned(self) -> None:
        start = AbsoluteCoordinate(0, 0, Orientation(0))
        stop = AbsoluteCoordinate(0, 0, Orientation(0))
        movement = AbsoluteMovement(start, stop)
        self.robot_coordinate.length = 10

        self.direct_driver.drive(movement, self.drivable)

        expected_calls = [call.translate(Angle(0), Distance(10))]
        actual_calls = self.drivable.method_calls
        self.assertListEqual(expected_calls, actual_calls)
