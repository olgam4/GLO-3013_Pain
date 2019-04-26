from logging import captureWarnings
from unittest import TestCase
from unittest.mock import patch, Mock

from communication.infrastructure.lightLED import LightLED

captureWarnings(True)


class TestLightLED(TestCase):
    def setUp(self) -> None:
        led_patcher = patch('communication.infrastructure.lightLED.Led')
        self.Led = led_patcher.start()
        self.addCleanup(led_patcher.stop)

        self.led = Mock()
        self.Led.return_value = self.led

        self.PIN = 17
        self.light = LightLED(self.PIN)

    def test_when_created_then_is_off(self) -> None:
        self.Led.assert_called_with(self.PIN)

    def test_when_turned_on_then_led_is_on(self) -> None:
        self.light.turn_on()

        self.assertTrue(self.led.on.called)

    def test_given_an_on_light_when_turned_off_then_is_off(self) -> None:
        self.light.turn_off()

        self.assertTrue(self.led.off.called)
