from unittest import TestCase
from unittest.mock import Mock

from mobility.domain.operation.rotateOperation import RotateOperation


class TestRotateOperation(TestCase):
    def setUp(self) -> None:
        self.angle = Mock()
        self.operation = RotateOperation(self.angle)

    def test_given_drivable_when_execute_then_drivable_rotates(self) -> None:
        drivable = Mock()

        self.operation.execute(drivable)

        drivable.rotate.assert_called_with(self.angle)
