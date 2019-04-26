from logging import getLogger, Logger
from threading import Event
from typing import Dict, Callable

from application.domain.iRobotWatcher import IRobotWatcher
from application.infrastructure.iCommandStateNotifier import ICommandStateNotifier
from communication.service.communicationService import CommunicationService
from communication.service.message import Message
from light.domain.light import Light
from light.service.lightService import LightService
from objective.domain.objective import Objective
from objective.service.objectiveService import ObjectiveService
from pathfinding.service.pathService import PathService
from pathfinding.service.pathfindingService import PathfindingService
from pathfinding.service.positionService import PositionService
from prehensor.domain.prehensor import Prehensor
from prehensor.service.prehensorService import PrehensorService
from vision.service.robotCameraService import RobotCameraService

logger: Logger = getLogger(__name__)


class RobotDisconnected(Exception):
    pass


class RobotWatcher(IRobotWatcher):
    def __init__(self, communication_service: CommunicationService, light_service: LightService,
                 command_state_notifier: ICommandStateNotifier, robot_camera_service: RobotCameraService,
                 pathfinding_service: PathfindingService, position_service: PositionService,
                 path_service: PathService, prehensor_service: PrehensorService,
                 objective_service: ObjectiveService) -> None:
        self._objective_service = objective_service
        self._prehensor_service = prehensor_service
        self._path_service = path_service
        self._position_service = position_service
        self._robot_camera_service = robot_camera_service
        self._communication_service = communication_service
        self._light_service = light_service
        self._pathfinding_service = pathfinding_service
        self._command_state_notifier = command_state_notifier
        self._handles: Dict[str, Callable[[Message], None]] = {}
        self._fill_handles()
        self._stopped = Event()

    def run(self) -> None:
        while not self._stopped.is_set():
            try:
                message = self._communication_service.receive_message()
                logger.info(message._data.keys())
                self._handles[message.title](message)
            except TimeoutError:
                pass

    def stop(self) -> None:
        self._stopped.set()

    def _fill_handles(self) -> None:
        self._handles["update"] = self._update
        self._handles["command_completed"] = self._command_completed
        self._handles["disconnect"] = self._disconnect
        self._handles["request_goal_pathable"] = self._pathable_goal
        self._handles["request_charge_station_pathable"] = self._pathable_charge_station
        self._handles["request_qr_code_pathable"] = self._pathable_qr_code
        self._handles["request_source_pathable"] = self._pathable_source
        self._handles["request_home_pathable"] = self._pathable_home
        self._handles["get_position"] = self._robot_position
        self._handles["full_path"] = self._full_path

    def _update(self, message: Message) -> None:
        try:
            light_on: bool = message.get_data("light_on")
            self._light_service.update_light(Light(light_on))
        except KeyError:
            pass
        try:
            image_data: str = message.get_data("image_data")
            self._robot_camera_service.update_image(image_data)
        except KeyError:
            pass
        try:
            capacitor_charge: float = message.get_data("capacitor_charge")
            self._prehensor_service.update_prehensor(Prehensor(capacitor_charge))
        except KeyError:
            pass
        try:
            objective_text: str = message.get_data("objective")
            self._objective_service.update_objective(Objective(objective_text))
        except KeyError:
            pass

    def _command_completed(self, message: Message) -> None:
        self._command_state_notifier.completed(message.get_data("command"))

    def _pathable_goal(self, message: Message) -> None:
        path = self._pathfinding_service.get_goal()
        data = path.serialize()
        self._communication_service.send_message(Message("goal_pathable", table=data))

    def _pathable_charge_station(self, message: Message) -> None:
        path = self._pathfinding_service.get_charge_station()
        data = path.serialize()
        self._communication_service.send_message(Message("charge_station_pathable", table=data))

    def _pathable_qr_code(self, message: Message) -> None:
        path = self._pathfinding_service.get_qr_code()
        data = path.serialize()
        self._communication_service.send_message(Message("qr_code_pathable", table=data))

    def _pathable_home(self, message: Message) -> None:
        path = self._pathfinding_service.get_home()
        data = path.serialize()
        self._communication_service.send_message(Message("home_pathable", table=data))

    def _pathable_source(self, message: Message) -> None:
        path = self._pathfinding_service.get_source()
        data = path.serialize()
        self._communication_service.send_message(Message("source_pathable", table=data))

    def _robot_position(self, message: Message) -> None:
        self._position_service.update_robot_position()

    def _full_path(self, message: Message):
        self._path_service.set_path(message.get_data("path"))

    def _disconnect(self, message: Message) -> None:
        raise RobotDisconnected()
