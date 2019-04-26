from threading import Event
from time import sleep

from application.domain.iRobotWorker import IRobotWorker
from communication.service.communicationService import CommunicationService
from communication.service.displayService import DisplayService
from communication.service.message import Message
from dexterity.domain.iChargeable import IChargeable
from vision.service.visionService import VisionService


class RobotWorker(IRobotWorker):
    PERIOD = 1

    def __init__(self, vision_service: VisionService, communication_service: CommunicationService,
                 display_service: DisplayService, chargeable: IChargeable):
        self._display_service = display_service
        self._communication_service = communication_service
        self._vision_service = vision_service
        self._chargeable = chargeable
        self._stopped = Event()

    def run(self) -> None:
        while not self._stopped.is_set():
            self._update_base()
            sleep(self.PERIOD)

    def stop(self) -> None:
        self._stopped.set()

    def _update_base(self) -> None:
        self._vision_service.update()
        update_message = Message("update", light_on=self._display_service.is_light_on(),
                                 image_data=self._vision_service.get_image(),
                                 capacitor_charge=self._chargeable.get_charge(),
                                 objective=self._vision_service.get_objective())
        self._communication_service.send_message(update_message)
