from application.domain.iObserver import IObserver
from communication.service.communicationService import CommunicationService
from communication.service.message import Message
from pathfinding.domain.position import Position
from vision.service.visionService import VisionService


class PositionService(IObserver):
    def __init__(self, vision_service: VisionService, communication_service: CommunicationService) -> None:
        self._vision_service = vision_service
        self._vision_service.attach(self)
        self._communication_service = communication_service

    def update(self) -> None:
        position = self._vision_service.get_robot()
        robot_position = Position(position.coordinate.to_centimeters(), position.orientation)
        data = robot_position.serialize()
        self._communication_service.send_message(Message("position", position=data))

    def update_robot_position(self) -> None:
        self._vision_service.update()
