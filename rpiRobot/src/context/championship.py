from application.domain.application import Application
from application.domain.iBaseWatcher import IBaseWatcher
from application.infrastructure.championshipBaseWatcher import ChampionshipBaseWatcher
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
from cortex.service.cortexService import CortexService
from dexterity.infrastructure.adcCharge import AdcCharge
from dexterity.service.dexterityService import DexterityService
from mobility.infrastructure.directDriver import DirectDriver
from mobility.infrastructure.positionDriver import PositionDriver
from mobility.service.mobilityService import MobilityService
from polling.service.pollingService import PollingService
from sight.infrastructure.pololuEyes import PololuEyes
from sight.service.sightService import SightService
from vision.infrastructure.openCvCameraCalibrationFactory import OpenCvCameraCalibrationFactory
from vision.infrastructure.openCvCameraFactory import OpenCvCameraFactory
from vision.infrastructure.openCvDestinationFinder import OpenCvDestinationFinder
from vision.infrastructure.openCvItemFinder import OpenCvItemFinder
from vision.infrastructure.openCvQrCodeReader import OpenCvQrCodeReader
from vision.service.objectiveParser import ObjectiveParser
from vision.service.visionService import VisionService


class Championship:
    def __init__(self, port):
        self._chargeable = AdcCharge()
        self._dexterity_service = DexterityService(GpioMapper.get_electromagnet_gpio())
        self._sight_service = SightService(PololuEyes())
        self._vision_service = VisionService(OpenCvCameraFactory(), OpenCvCameraCalibrationFactory(),
                                             OpenCvQrCodeReader(), OpenCvItemFinder(), OpenCvDestinationFinder(),
                                             ObjectiveParser())
        self._communication_service = CommunicationService(SocketBaseConnector(port))
        self._position_service = PositionService(self._communication_service)
        self._movement_driver = PositionDriver(self._position_service, DirectDriver())
        self._mobility_service = MobilityService(GpioMapper.get_drivable_gpio(), self._movement_driver)
        self._display_service = DisplayService(GpioMapper.get_light_led())
        self._pathable_communicator = PathableCommunicator(self._communication_service)
        self._pathable_catalog = PathableCatalog(self._pathable_communicator)
        self._direction_cortex = DirectionCortex(self._pathable_catalog, self._position_service, self._mobility_service,
                                                 self._pathable_communicator)
        self._nap_cortex = NapCortex(self._mobility_service, self._direction_cortex)
        self._visual_cortex = VisualCortex(self._vision_service, self._sight_service)
        self._item_chooser = PollingService()
        self._dexterity_cortex = DexterityCortex(self._mobility_service, self._dexterity_service,
                                                 self._direction_cortex, self._visual_cortex, self._item_chooser)
        self._communication_cortex = CommunicationCortex(self._display_service, self._communication_service)

    def application(self) -> Application:
        robot_worker = self.make_robot_worker()
        cerebrum = self.make_cerebrum()
        base_watcher = self.make_base_watcher()
        return Application(cerebrum, robot_worker, base_watcher)

    def make_base_watcher(self) -> IBaseWatcher:
        return ChampionshipBaseWatcher(self._communication_service, self._pathable_catalog, PathableFactory(),
                                       self._position_service, self._nap_cortex)

    def make_cerebrum(self) -> CortexService:
        cortex = Cortex(self._communication_cortex, self._visual_cortex, self._direction_cortex, self._nap_cortex,
                        self._dexterity_cortex)
        return CortexService(cortex)

    def make_robot_worker(self):
        return RobotWorker(self._vision_service, self._communication_service, self._display_service, self._chargeable)
