from unittest import TestCase
from unittest.mock import Mock

from mobility.domain.operation.translateOperation import TranslateOperation


class TestTranslateOperation(TestCase):
    def setUp(self) -> None:
        self.angle = Mock()
        self.movement = Mock()
        self.operation = TranslateOperation(self.angle, self.movement)

    def test_given_drivable_when_executed_then_drivable_moves(self) -> None:
        drivable = Mock()

        self.operation.execute(drivable)

        drivable.translate.assert_called_with(self.angle, self.movement)
