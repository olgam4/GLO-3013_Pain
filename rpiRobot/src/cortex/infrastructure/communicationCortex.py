from time import sleep

from communication.service.communicationService import CommunicationService
from communication.service.displayService import DisplayService
from cortex.domain.iCommunicationCortex import ICommunicationCortex


class CommunicationCortex(ICommunicationCortex):
    def __init__(self, display_service: DisplayService, communication_service: CommunicationService):
        self._display_service = display_service
        self._display_service.set_light_off()
        self._communication_service = communication_service

    def announce_win(self) -> None:
        self._display_service.set_light_on()
        sleep(5)
        self._display_service.set_light_off()
