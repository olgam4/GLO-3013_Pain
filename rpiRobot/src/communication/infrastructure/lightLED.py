from logging import getLogger

from communication.domain.iLight import ILight
from gpioPain.led import Led

logger = getLogger(__name__)


class LightLED(ILight):
    def __init__(self, pin: int):
        self._led = Led(pin)

    @property
    def is_on(self) -> bool:
        return self._led.is_lit

    def turn_on(self):
        self._led.on()

    def turn_off(self):
        self._led.off()
