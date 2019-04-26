from logging import getLogger

from serial import Serial, SerialException

logger = getLogger(__name__)


class UartSerial:
    def __init__(self):
        try:
            self._serial = Serial(port='/dev/serial0', timeout=1)
        except SerialException:
            logger.warning("Could not connect uart port")
            self._serial = None

    def send(self, data: bytes) -> None:
        if self._serial:
            self._serial.write(data)

    def recv(self) -> bytes:
        if self._serial:
            read = b''
            if self._serial:
                read = self._serial.read(1)
            if len(read) == 0:
                raise TimeoutError
            return read
        else:
            # TODO move to consts package and load from context
            return b'7'
