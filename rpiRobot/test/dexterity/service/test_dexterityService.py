from unittest import TestCase
from unittest.mock import Mock

from dexterity.service.dexterityService import DexterityService


class TestDexterityService(TestCase):
    def setUp(self) -> None:
        self.prehensor = Mock()
        self.service = DexterityService(self.prehensor)

    def test_when_grabbing_then_prehensor_grabs(self) -> None:
        self.service.grab()

        self.assertTrue(self.prehensor.grab.called)

    def test_when_letting_go_then_prehensor_lets_go(self) -> None:
        self.service.let_go()

        self.assertTrue(self.prehensor.let_go.called)
