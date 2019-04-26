from threading import Lock
from typing import Callable, Any

from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from remote.service.remoteService import RemoteService
from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner


class RemoteSubroutineRunner(ISubroutineRunner):
    def __init__(self, remote_service: RemoteService) -> None:
        self._remote_service = remote_service
        self._callback: CommandCallback = None
        self._busy = False
        self._busy_lock = Lock()

    def execute_charge_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        self._start_command(self._remote_service.execute_charge_subroutine, callback)

    def execute_go_home_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        self._start_command(self._remote_service.execute_go_home_subroutine, callback)

    def execute_read_qr_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        self._start_command(self._remote_service.execute_read_qr_subroutine, callback)

    def execute_grab_subroutine(self, target: str, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        self._start_command(self._remote_service.execute_grab_subroutine, callback, target=target)

    def execute_drop_subroutine(self, target: str, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        self._start_command(self._remote_service.execute_drop_subroutine, callback, target=target)

    def execute_switch_light_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        self._start_command(self._remote_service.execute_switch_light_subroutine, callback)

    def execute_directional_movement(self, direction: str, speed: str, distance: float,
                                     callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        self._start_command(self._remote_service.execute_directional_movement, callback,
                            direction=direction, speed=speed, distance=distance)

    def execute_rotational_movement(self, angle: float, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        self._start_command(self._remote_service.execute_rotational_movement, callback, angle=angle)

    def execute_activate_magnet(self, callback: CommandCallback) -> None:
        self._start_command(self._remote_service.execute_activate_magnet, callback)

    def execute_deactivate_magnet(self, callback: CommandCallback) -> None:
        self._start_command(self._remote_service.execute_deactivate_magnet, callback)

    def execute_discharge_magnet(self, callback: CommandCallback) -> None:
        self._start_command(self._remote_service.execute_discharge_magnet, callback)

    def execute_update_directions_subroutine(self, callback: CommandCallback) -> None:
        self._start_command(self._remote_service.execute_update_directions, callback)

    def execute_championship_subroutine(self, callback: CommandCallback):
        self._start_command(self._remote_service.execute_championship, callback)

    def execute_look_down(self, callback: CommandCallback) -> None:
        self._start_command(self._remote_service.execute_look_down, callback)

    def execute_look_ahead(self, callback: CommandCallback) -> None:
        self._start_command(self._remote_service.execute_look_ahead, callback)

    def _command_done(self, status: CommandStatus) -> None:
        with self._busy_lock:
            self._busy = False
            self._callback(status)

    def _start_command(self, function: Callable[[Any], None], callback: CommandCallback, **kwargs) -> None:
        """

        :raises BlockingIOError: command already running
        """
        with self._busy_lock:
            if self._busy:
                raise BlockingIOError()
            self._busy = True
        self._callback = callback
        kwargs["callback"] = self._command_done
        function(**kwargs)
