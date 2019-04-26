from communication.infrastructure.lightLED import LightLED
from dexterity.infrastructure.electromagnetGPIO import ElectromagnetGPIO
from mobility.infrastructure.drivableGPIO import DrivableGPIO
from mobility.infrastructure.uartSerial import UartSerial


class GpioMapper:
    _HOLD_PIN = 13
    _GRAB_PIN = 19
    _WIN_LED = 26

    @classmethod
    def get_drivable_gpio(cls) -> DrivableGPIO:
        return DrivableGPIO(UartSerial())

    @classmethod
    def get_light_led(cls) -> LightLED:
        return LightLED(cls._WIN_LED)

    @classmethod
    def get_electromagnet_gpio(cls) -> ElectromagnetGPIO:
        return ElectromagnetGPIO(cls._HOLD_PIN, cls._GRAB_PIN)
