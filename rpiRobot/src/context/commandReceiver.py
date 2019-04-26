from application.domain.application import Application
from application.domain.iBaseWatcher import IBaseWatcher
from application.domain.iCerebrum import ICerebrum
from application.infrastructure.championshipBaseWatcher import ChampionshipBaseWatcher
from application.infrastructure.remoteBaseWatcher import RemoteBaseWatcher
from application.infrastructure.remoteCerebrum import RemoteCerebrum
from application.infrastructure.robotWorker import RobotWorker
from communication.infrastructure.socketBaseConnector import SocketBaseConnector
from communication.service.communicationService import CommunicationService
from communication.service.displayService import DisplayService
from communication.service.positionService import PositionService
from context.gpioMapper import GpioMapper
from cortex.domain.cortex import Cortex
from cortex.domain.dexterityCortex import DexterityCortex
from cortex.domain.directionCortex import DirectionCortex
from cortex.domain.pathableCatalog import PathableCatalog
from cortex.infrastructure.communicationCortex import CommunicationCortex
from cortex.infrastructure.napCortex import NapCortex
from cortex.infrastructure.pathableCommunicator import PathableCommunicator
from cortex.infrastructure.pathableFactory import PathableFactory
from cortex.infrastructure.visualCortex import VisualCortex
from dexterity.infrastructure.adcCharge import AdcCharge
from dexterity.service.dexterityService import DexterityService
from mobility.infrastructure.directDriver import DirectDriver
from mobility.infrastructure.positionDriver import PositionDriver
from mobility.service.mobilityService import MobilityService
from polling.service.pollingService import PollingService
from remote.messageTranslator import MessageTranslator
from remote.remoteService import RemoteService
from sight.infrastructure.pololuEyes import PololuEyes
from sight.service.sightService import SightService
from vision.infrastructure.openCvCameraCalibrationFactory import OpenCvCameraCalibrationFactory
from vision.infrastructure.openCvCameraFactory import OpenCvCameraFactory
from vision.infrastructure.openCvDestinationFinder import OpenCvDestinationFinder
from vision.infrastructure.openCvItemFinder import OpenCvItemFinder
from vision.infrastructure.openCvQrCodeReader import OpenCvQrCodeReader
from vision.service.objectiveParser import ObjectiveParser
from vision.service.visionService import VisionService


class CommandReceiver:
    def __init__(self, port: int) -> None:
        self._chargeable = AdcCharge()
        self._dexterity_service = DexterityService(GpioMapper.get_electromagnet_gpio())
        self._sight_service = SightService(PololuEyes())
        self._vision_service = VisionService(OpenCvCameraFactory(), OpenCvCameraCalibrationFactory(),
                                             OpenCvQrCodeReader(), OpenCvItemFinder(), OpenCvDestinationFinder(),
                                             ObjectiveParser())
        self._display_service = DisplayService(GpioMapper.get_light_led())
        self._base_connector = SocketBaseConnector(port)
        self._communication_service = CommunicationService(self._base_connector)
        self._position_service = PositionService(self._communication_service)
        self._drivable = GpioMapper.get_drivable_gpio()
        self._movement_driver = PositionDriver(self._position_service, DirectDriver())
        self._mobility_service = MobilityService(self._drivable, self._movement_driver)
        self._remote_service = RemoteService(self._mobility_service)
        self._message_translator = MessageTranslator()
        self._remote_cerebrum = RemoteCerebrum()
        self._pathable_communicator = PathableCommunicator(self._communication_service)
        self._pathable_catalog = PathableCatalog(self._pathable_communicator)
        self._direction_cortex = DirectionCortex(self._pathable_catalog, self._position_service,
                                                 self._mobility_service, self._pathable_communicator)
        self._direction_cortex = DirectionCortex(self._pathable_catalog, self._position_service, self._mobility_service,
                                                 self._pathable_communicator)
        self._nap_cortex = NapCortex(self._mobility_service, self._direction_cortex)
        self._visual_cortex = VisualCortex(self._vision_service, self._sight_service)
        self._item_chooser = PollingService()
        self._dexterity_cortex = DexterityCortex(self._mobility_service, self._dexterity_service,
                                                 self._direction_cortex, self._visual_cortex, self._item_chooser)

    def application(self) -> Application:
        remote_cerebrum = self._make_remote_cerebrum()
        robot_worker = self._make_robot_worker()
        base_watcher = self.make_base_watcher()
        return Application(remote_cerebrum, robot_worker, base_watcher)

    def make_base_watcher(self) -> IBaseWatcher:
        cortex = self._make_cortex()
        championship_watcher = ChampionshipBaseWatcher(self._communication_service, self._pathable_catalog,
                                                       PathableFactory(), self._position_service,
                                                       self._nap_cortex)
        return RemoteBaseWatcher(self._communication_service, self._remote_service, self._display_service,
                                 self._message_translator, self._dexterity_service, self._remote_cerebrum,
                                 cortex, self._direction_cortex, championship_watcher, self._sight_service)

    def _make_remote_cerebrum(self) -> ICerebrum:
        return self._remote_cerebrum

    def _make_robot_worker(self) -> RobotWorker:
        return RobotWorker(self._vision_service, self._communication_service, self._display_service, self._chargeable)

    def _make_cortex(self) -> Cortex:
        communication_cortex = CommunicationCortex(self._display_service, self._communication_service)
        return Cortex(communication_cortex, self._visual_cortex, self._direction_cortex, self._nap_cortex,
                      self._dexterity_cortex)
