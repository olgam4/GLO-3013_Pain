from logging import getLogger
from threading import Event

from application.domain.iBaseWatcher import IBaseWatcher
from communication.service.communicationService import CommunicationService
from communication.service.message import Message
from communication.service.positionService import PositionService
from cortex.domain.iPathableFactory import IPathableFactory
from cortex.infrastructure.napCortex import NapCortex
from cortex.domain.pathableCatalog import PathableCatalog

logger = getLogger(__name__)


class ChampionshipBaseWatcher(IBaseWatcher):
    def __init__(self, communication_service: CommunicationService, pathable_catalog: PathableCatalog,
                 pathable_factory: IPathableFactory, position_service: PositionService, nap_cortex: NapCortex) -> None:
        self._communication_service = communication_service
        self._pathable_catalog = pathable_catalog
        self._pathable_factory = pathable_factory
        self._position_service = position_service
        self._nap_cortex = nap_cortex
        self._stopped = Event()
        self._handles = {}
        self._fill_handles()

    def run(self) -> None:
        while not self._stopped.is_set():
            message = self._communication_service.receive_message()
            logger.debug(message.serialize())
            try:
                self._handles[message.title](message)
            except KeyError:
                logger.warning(format("Invalid operation {}", message.title))

    def stop(self) -> None:
        self._stopped.set()

    def _fill_handles(self) -> None:
        self._handles["goal_pathable"] = self.set_goal_pathable
        self._handles["charge_station_pathable"] = self.set_charge_station_pathable
        self._handles["qr_code_pathable"] = self.set_qr_code_pathable
        self._handles["home_pathable"] = self.set_home_pathable
        self._handles["source_pathable"] = self.set_source_pathable
        self._handles["position"] = self.update_position
        self._handles["start_charging"] = self.start_charging
        self._handles["lost_connection"] = self.lost_connection
        self._handles["charge_done"] = self.charge_done

    def update_position(self, message: Message) -> None:
        self._position_service.set_position(message.get_data("position"))

    def set_goal_pathable(self, message: Message) -> None:
        pathable = self._pathable_factory.create_from(message.get_data('table'))
        self._pathable_catalog.goal = pathable

    def set_charge_station_pathable(self, message: Message) -> None:
        pathable = self._pathable_factory.create_from(message.get_data('table'))
        self._pathable_catalog.charge_station = pathable

    def set_qr_code_pathable(self, message: Message) -> None:
        pathable = self._pathable_factory.create_from(message.get_data('table'))
        self._pathable_catalog.qr_code = pathable

    def set_home_pathable(self, message: Message) -> None:
        pathable = self._pathable_factory.create_from(message.get_data('table'))
        self._pathable_catalog.home = pathable

    def set_source_pathable(self, message: Message) -> None:
        pathable = self._pathable_factory.create_from(message.get_data('table'))
        self._pathable_catalog.source = pathable

    def start_charging(self, message: Message) -> None:
        self._nap_cortex.start_charging()

    def lost_connection(self, message: Message) -> None:
        self._nap_cortex.lost_connection()

    def charge_done(self, message: Message) -> None:
        self._nap_cortex.charge_done()
