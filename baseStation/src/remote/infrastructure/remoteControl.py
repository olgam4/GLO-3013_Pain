from typing import Dict

from application.infrastructure.iCommandStateNotifier import ICommandStateNotifier
from communication.service.communicationService import CommunicationService
from communication.service.message import Message
from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from remote.domain.iRemoteControl import IRemoteControl


class RemoteControl(IRemoteControl, ICommandStateNotifier):
    def __init__(self, communication_service: CommunicationService) -> None:
        self._communication_service = communication_service
        self._callback_commands: Dict[str, CommandCallback] = {}

    def execute_charge_subroutine(self, callback: CommandCallback) -> None:
        command = "charge_subroutine"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_go_home_subroutine(self, callback: CommandCallback) -> None:
        command = "go_home_subroutine"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_read_qr_subroutine(self, callback: CommandCallback) -> None:
        command = "read_qr_subroutine"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_grab_subroutine(self, target: str, callback: CommandCallback) -> None:
        command = "grab_subroutine"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command, target=target))

    def execute_drop_subroutine(self, target: str, callback: CommandCallback) -> None:
        command = "drop_subroutine"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command, target=target))

    def execute_switch_light_subroutine(self, callback: CommandCallback) -> None:
        command = "switch_light_subroutine"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_directional_movement(self, direction: str, speed: str, distance: float,
                                     callback: CommandCallback) -> None:
        command = "directional_movement"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command, direction=direction, speed=speed, distance=distance))

    def execute_rotational_movement(self, angle: float, callback: CommandCallback) -> None:
        command = "rotational_movement"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command, angle=angle))

    def execute_activate_magnet(self, callback: CommandCallback) -> None:
        command = "activate_magnet"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_deactivate_magnet(self, callback: CommandCallback) -> None:
        command = "deactivate_magnet"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_discharge_magnet(self, callback: CommandCallback) -> None:
        command = "discharge_magnet"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_update_directions(self, callback: CommandCallback) -> None:
        command = "update_directions"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_championship(self, callback: CommandCallback) -> None:
        command = "championship"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_look_down(self, callback: CommandCallback) -> None:
        command = "look_down"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def execute_look_ahead(self, callback: CommandCallback) -> None:
        command = "look_ahead"
        self._callback_commands[command] = callback
        self._communication_service.send_message(Message(command))

    def completed(self, command: str) -> None:
        self._callback_commands[command](CommandStatus.completed)

    def errored(self, command: str) -> None:
        self._callback_commands[command](CommandStatus.errored)

    def cancelled(self, command: str) -> None:
        self._callback_commands[command](CommandStatus.cancelled)
