from logging import getLogger
from typing import Any, Union

from gpiozero import BadPinFactory, LED

logger = getLogger(__name__)


class Led:
    def __init__(self, pin: Union[int, str], active_high=True, initial_value=False) -> None:
        try:
            self._led = LED(pin, active_high=active_high, initial_value=initial_value)
        except BadPinFactory:
            logger.warning("no gpio found")
            self._led = None

    @property
    def pin(self) -> Any:
        if self._led:
            return self._led.pin

    @property
    def is_lit(self) -> bool:
        if self._led:
            return self._led.is_lit
        return False

    @property
    def value(self) -> int:
        if self._led:
            return self._led.value
        return 0

    @value.setter
    def value(self, value) -> None:
        if self._led:
            self._led.value = value

    def close(self) -> None:
        if self._led:
            self._led.close()

    def on(self) -> None:
        if self._led:
            self._led.on()

    def off(self) -> None:
        if self._led:
            self._led.off()

    def toggle(self) -> None:
        if self._led:
            self._led.toggle()

    def blink(self) -> None:
        if self._led:
            self._led.blink()
