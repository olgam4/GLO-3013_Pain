from communication.service.communicationService import CommunicationService
from communication.service.message import Message
from cortex.domain.iPathableCommunicator import IPathableCommunicator
from cortex.domain.path.absolutePath import AbsolutePath


class PathableCommunicator(IPathableCommunicator):
    def __init__(self, communication_service: CommunicationService) -> None:
        self._communication_service = communication_service

    def request_charge_station_pathable(self) -> None:
        self._communication_service.send_message(Message("request_charge_station_pathable"))

    def request_qr_code_pathable(self) -> None:
        self._communication_service.send_message(Message("request_qr_code_pathable"))

    def request_source_pathable(self) -> None:
        self._communication_service.send_message(Message("request_source_pathable"))

    def request_goal_pathable(self) -> None:
        self._communication_service.send_message(Message("request_goal_pathable"))

    def request_home_pathable(self) -> None:
        self._communication_service.send_message(Message("request_home_pathable"))

    def send_full_path(self, path: AbsolutePath) -> None:
        data = path.serialize()
        self._communication_service.send_message(Message("full_path", path=data))
