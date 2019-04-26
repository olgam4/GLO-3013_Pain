from math import pi
from threading import Event, Thread
from time import sleep

from cortex.domain.directionCortex import DirectionCortex
from cortex.domain.iNapCortex import INapCortex
from mobility.domain.angle import Angle
from mobility.domain.distance import Distance
from mobility.domain.operation.translateOperation import TranslateOperation
from mobility.service.mobilityService import MobilityService

DISTANCE_FROM_BED = 16


class NapCortex(INapCortex):
    def __init__(self, mobility_service: MobilityService, direction_cortex: DirectionCortex) -> None:
        self._mobility_service = mobility_service
        self._direction_cortex = direction_cortex
        self._charged = Event()
        self._charged.set()
        self._charging = Event()

    def recharge(self) -> None:
        self._charged.clear()
        self._align_on_charge_station()
        self._charged.wait()
        self._wake_up()

    def _wake_up(self):
        self._mobility_service.operate([TranslateOperation(Angle(0), Distance(DISTANCE_FROM_BED))])

    def start_charging(self) -> None:
        if self._charged.is_set():
            return
        self._charging.set()
        self._mobility_service.brake()

    def lost_connection(self) -> None:
        if self._charging.is_set():
            self._align_on_charge_station()

    def charge_done(self) -> None:
        self._charging.clear()
        self._charged.set()

    def _align_on_charge_station(self) -> None:
        self._alignment_thread = Thread(target=self._align_on_charge_station_func)
        self._alignment_thread.start()

    def _align_on_charge_station_func(self) -> None:
        self._charging.clear()
        while not self._charging.is_set():
            self._direction_cortex.reach_charge()
            self._mobility_service.operate([TranslateOperation(Angle(pi), Distance(DISTANCE_FROM_BED))])
            sleep(1)
