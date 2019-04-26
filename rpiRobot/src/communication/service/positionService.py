from threading import Event

from communication.service.communicationService import CommunicationService
from communication.service.message import Message
from coordinate.absoluteCoordinate import AbsoluteCoordinate


class PositionService:
    def __init__(self, communication_service: CommunicationService) -> None:
        self._communication_service = communication_service
        self._position_received = Event()
        self._position = AbsoluteCoordinate.zero()

    def set_position(self, position: str) -> None:
        self._position = AbsoluteCoordinate.deserialize(position)
        self._position_received.set()

    def get_position(self) -> AbsoluteCoordinate:
        self._communication_service.send_message(Message("get_position"))
        self._position_received.clear()
        self._position_received.wait()
        return self._position
