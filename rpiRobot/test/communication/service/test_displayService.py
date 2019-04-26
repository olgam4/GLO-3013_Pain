from unittest import TestCase
from unittest.mock import Mock

from communication.service.displayService import DisplayService


class TestDisplayService(TestCase):
    def setUp(self) -> None:
        self.light = Mock()
        self.service = DisplayService(light=self.light)

    def test_when_light_is_on_then_light_is_on(self) -> None:
        self.light.is_on = True

        self.assertTrue(self.service.is_light_on())

    def test_given_light_on_when_switch_then_turn_it_off(self) -> None:
        self.light.is_on = True

        self.service.switch_light()

        self.assertTrue(self.light.turn_off.called)

    def test_given_light_off_when_switch_then_turn_it_on(self) -> None:
        self.light.is_on = False

        self.service.switch_light()

        self.assertTrue(self.light.turn_on.called)

    def test_when_set_light_on_then_light_turned_on(self) -> None:
        self.service.set_light_on()

        self.assertTrue(self.light.turn_on.called)

    def test_when_set_light_off_then_light_turned_off(self) -> None:
        self.service.set_light_off()

        self.assertTrue(self.light.turn_off.called)
