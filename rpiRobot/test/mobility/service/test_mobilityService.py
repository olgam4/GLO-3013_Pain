from unittest import TestCase
from unittest.mock import Mock, call

from cortex.domain.path.absolutePath import AbsolutePath
from mobility.service.mobilityService import MobilityService


class TestMobilityService(TestCase):
    def setUp(self) -> None:
        self.drivable = Mock()
        self.movement_driver = Mock()
        self.operation = Mock()
        self.movement_driver.calculate.return_value = [self.operation]
        self.service = MobilityService(self.drivable, self.movement_driver)

    def test_givenPath_whenDriven_thenOperationCalculatorCalculatesOperations(self) -> None:
        movement3 = Mock()
        movement2 = Mock()
        movement1 = Mock()
        path = AbsolutePath([movement1, movement2, movement3])

        self.service.drive(path)

        expected_calls = [call.drive(movement1, self.drivable),
                          call.drive(movement2, self.drivable),
                          call.drive(movement3, self.drivable)]
        actual_calls = self.movement_driver.method_calls
        self.assertListEqual(expected_calls, actual_calls)

    def test_givenPathOfSingleMovement_whenDriven_thenOperationExecutesWithDrivable(self) -> None:
        operations = [self.operation]

        self.service.operate(operations)

        self.operation.execute.assert_called_with(self.drivable)
