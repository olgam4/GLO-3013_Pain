from logging import getLogger
from threading import Event
from typing import Dict, Callable

from application.domain.iChargeStationWatcher import IChargeStationWatcher
from communication.service.communicationService import CommunicationService
from communication.service.message import Message
from prehensor.domain.iChargeStation import IChargeStation

logger = getLogger(__name__)


class ChargeStationWatcher(IChargeStationWatcher):
    def __init__(self, communication_service: CommunicationService, charge_station: IChargeStation) -> None:
        self._communication_service = communication_service
        self._charge_station = charge_station
        self._handles: Dict[str, Callable[[], None]] = {}
        self._fill_handles()
        self._stopped = Event()

    def run(self) -> None:
        while not self._stopped.is_set():
            try:
                message = self._charge_station.recv()
                logger.warning(message)
                self._handles[message]()
            except TimeoutError:
                pass
            except KeyError:
                pass

    def stop(self) -> None:
        self._stopped.set()

    def _fill_handles(self) -> None:
        self._handles["contact"] = self._start_charging
        self._handles["contactlost"] = self._lost_connection
        self._handles["charged"] = self._charge_done

    def _start_charging(self) -> None:
        self._communication_service.send_message(Message("start_charging"))

    def _lost_connection(self) -> None:
        self._communication_service.send_message(Message("lost_connection"))

    def _charge_done(self) -> None:
        self._communication_service.send_message(Message("charge_done"))
