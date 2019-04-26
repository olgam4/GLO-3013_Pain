from logging import getLogger
from math import pi
from struct import pack, unpack
from threading import Event, Thread
from time import sleep

from mobility.domain.angle import Angle
from mobility.domain.distance import Distance
from mobility.domain.iDrivable import IDrivable
from mobility.infrastructure.uartSerial import UartSerial

logger = getLogger(__name__)


class DrivableGPIO(IDrivable):
    def __init__(self, port: UartSerial) -> None:
        self._port = port
        self._stopped = Event()
        self._movement_finished = Event()
        self._wheels_watcher_thread = Thread(target=self._wheels_watcher, daemon=True)
        self._wheels_watcher_thread.start()

    def translate(self, angle: Angle, distance: Distance) -> None:
        data = pack('c', b'T')
        data += pack('f', angle.radians)
        data += pack('f', distance.centimeters)
        logger.debug("angle: {} distance: {} => {}".format(angle.degrees, distance.centimeters, data))
        self._port.send(data)
        self._wait_complete_translation(distance)

    def careful(self, angle: Angle, distance: Distance) -> None:
        data = pack('c', b'C')
        data += pack('f', angle.radians)
        data += pack('f', distance.centimeters)
        logger.debug("angle: {} distance: {} => {}".format(angle.degrees, distance.centimeters, data))
        self._port.send(data)
        self._wait_complete_careful(distance)

    def rotate(self, angle: Angle) -> None:
        data = pack('c', b'R')
        data += pack('f', angle.radians)
        data += pack('f', 0)
        logger.debug("angle: {} => {}".format(angle.degrees, data))
        self._port.send(data)
        self._wait_complete_rotation(angle)

    def brake(self) -> None:
        data = pack('c', b'T')
        data += pack('f', 0)
        data += pack('f', 0)
        self._port.send(data)

    def stop(self) -> None:
        self._stopped.set()

    @staticmethod
    def _wait_complete_rotation(angle: Angle) -> None:
        # TODO use angle and speed to calculate time to wait
        nb_turns = angle.radians / (2 * pi)
        distance = nb_turns * 60
        nap_time = abs(distance / 3.33)
        # logger.debug("gonna sleep for {}seconds".format(nap_time))
        sleep(nap_time)

    @staticmethod
    def _wait_complete_translation(distance: Distance) -> None:
        sleep(distance.centimeters / 10)

    @staticmethod
    def _wait_complete_careful(distance: Distance) -> None:
        sleep(distance.centimeters / 3.33)

    def _wheels_watcher(self) -> None:
        while not self._stopped.is_set():
            try:
                response = self._port.recv()
                data = unpack('c', response)
                if data[0].decode() == '7':
                    self._movement_finished.set()
            except TimeoutError:
                pass
