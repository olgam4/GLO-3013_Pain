from logging import getLogger
from time import sleep

from serial import SerialException

from sight.domain.iEyes import IEyes
from sight.infrastructure.maestro import Controller

logger = getLogger(__name__)


class PololuEyes(IEyes):
    accel = 10
    speed = 50

    def __init__(self) -> None:
        self._with = False
        self._servo = None

    def __enter__(self):
        self._with = True
        try:
            self._servo = Controller()
            self._servo.setAccel(0, self.accel)
            self._servo.setAccel(1, self.accel)
            self._servo.setSpeed(0, self.speed)
            self._servo.setSpeed(1, self.speed)
        except SerialException:
            logger.warning('Could not connect pololu')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._servo:
            self._servo.close()
        self._servo = None
        self._with = False

    def look_ahead(self) -> None:
        if not self._with:
            logger.error("Resource servo not found")
            return
        if self._servo:
            # could go from 1000 to 11999
            self._servo.setTarget(0, 6000)
            self._servo.setTarget(1, 6000)
            sleep(4)

    def look_down(self) -> None:
        if not self._with:
            logger.error("Resource servo not found")
            return
        if self._servo:
            # could go from 1000 to 11999
            self._servo.setTarget(0, 6000)
            self._servo.setTarget(1, 3000)
            sleep(5)


if __name__ == "__main__":
    eyes = PololuEyes()
    eyes.look_down()
    eyes.look_down()
    while True:
        cmd = input('enter command(d-down|u-up|e-exit): ')
        with eyes:
            if cmd == 'd':
                eyes.look_down()
            elif cmd == 'u':
                eyes.look_ahead()
            elif cmd == 'e':
                break
