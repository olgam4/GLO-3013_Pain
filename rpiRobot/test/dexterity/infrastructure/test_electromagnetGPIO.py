from unittest import TestCase
from unittest.mock import patch, Mock, DEFAULT, call

from dexterity.infrastructure.electromagnetGPIO import ElectromagnetGPIO


class TestElectromagnetGPIO(TestCase):
    def setUp(self) -> None:
        led_patcher = patch('dexterity.infrastructure.electromagnetGPIO.Led')
        self.Led = led_patcher.start()
        self.addCleanup(led_patcher.stop)

        self.hold_pin = 5
        self.hold_led = Mock()
        self.grab_pin = 6
        self.grab_led = Mock()
        self.Led.side_effect = self.mock_return

        self.magnet = ElectromagnetGPIO(self.hold_pin, self.grab_pin)

    def mock_return(self, pin_number, **kwargs) -> Mock:
        if pin_number == self.hold_pin:
            return self.hold_led
        if pin_number == self.grab_pin:
            return self.grab_led
        return DEFAULT

    def test_when_created_then_grab_led_is_active_high(self) -> None:
        self.Led.assert_called_with(self.grab_pin)

    def test_when_grab_then_hold_led_is_set_on(self) -> None:
        self.magnet.grab()

        self.assertTrue(self.hold_led.on.called)

    def test_when_grab_then_grab_led_is_set_on_then_off(self) -> None:
        self.magnet.grab()

        expected_calls = [call.on, call.off]
        self.grab_led.assert_has_calls(expected_calls)

    def test_when_let_go_then_hold_led_is_set_off(self) -> None:
        self.magnet.let_go()

        self.assertTrue(self.hold_led.off.called)
