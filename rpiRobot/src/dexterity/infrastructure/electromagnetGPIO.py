from logging import getLogger
from time import sleep

from dexterity.domain.iPrehensor import IPrehensor
from gpioPain.led import Led

logger = getLogger(__name__)


class ElectromagnetGPIO(IPrehensor):
    def __init__(self, hold_pin: int, grab_pin: int) -> None:
        self._hold = Led(hold_pin)
        self._grab = Led(grab_pin)

    def grab(self) -> None:
        logger.debug("grab")
        self._hold.on()
        self._grab.on()
        sleep(0.05)
        self._grab.off()

    def let_go(self) -> None:
        logger.debug("let_go")
        self._grab.off()
        self._hold.off()
        sleep(3)

    def discharge(self) -> None:
        logger.debug("discharge")
        self._grab.on()


if __name__ == "__main__":
    hold_pin_selection = int(input("Choose the hold pin:"))

    grab_pin_selection = int(input("Choose the grab pin:"))

    magnet = ElectromagnetGPIO(hold_pin_selection, grab_pin_selection)
    while True:
        print("Enter a command ( g || d ):")
        cmd = input()
        if cmd == "g":
            magnet.grab()
        if cmd == "d":
            magnet.let_go()
