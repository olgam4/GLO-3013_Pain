from logging import getLogger
from time import sleep

from serial import Serial, SerialException

from prehensor.domain.iChargeStation import IChargeStation

logger = getLogger(__name__)


class ChargeStation(IChargeStation):
    timeout = 1

    def __init__(self) -> None:
        try:
            self._charge_station = Serial('/dev/ttyACM0', timeout=self.timeout)
        except SerialException as e:
            print(e)
            logger.warning("no serial port found")
            self._charge_station = None

    def recv(self) -> str:
        if self._charge_station:
            data = self._charge_station.readline()[:-2].decode()
            if data == "":
                raise TimeoutError
            return data
        sleep(self.timeout)
        raise TimeoutError


if __name__ == "__main__":
    charge_station = ChargeStation()
    print(charge_station.recv())
