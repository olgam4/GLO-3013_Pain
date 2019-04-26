from remote.domain.commandCallback import CommandCallback
from remote.domain.iRemoteControl import IRemoteControl


class RemoteService:
    def __init__(self, remote_control: IRemoteControl) -> None:
        self._remote_control = remote_control

    def execute_charge_subroutine(self, callback: CommandCallback) -> None:
        self._remote_control.execute_charge_subroutine(callback)

    def execute_go_home_subroutine(self, callback: CommandCallback) -> None:
        self._remote_control.execute_go_home_subroutine(callback)

    def execute_read_qr_subroutine(self, callback: CommandCallback) -> None:
        self._remote_control.execute_read_qr_subroutine(callback)

    def execute_grab_subroutine(self, target: str, callback: CommandCallback) -> None:
        self._remote_control.execute_grab_subroutine(target, callback)

    def execute_drop_subroutine(self, target: str, callback: CommandCallback) -> None:
        self._remote_control.execute_drop_subroutine(target, callback)

    def execute_switch_light_subroutine(self, callback: CommandCallback) -> None:
        self._remote_control.execute_switch_light_subroutine(callback)

    def execute_directional_movement(self, direction: str, speed: str, distance: float,
                                     callback: CommandCallback) -> None:
        self._remote_control.execute_directional_movement(direction, speed, distance, callback)

    def execute_rotational_movement(self, angle: float, callback: CommandCallback) -> None:
        self._remote_control.execute_rotational_movement(angle, callback)

    def execute_activate_magnet(self, callback: CommandCallback) -> None:
        self._remote_control.execute_activate_magnet(callback)

    def execute_deactivate_magnet(self, callback: CommandCallback) -> None:
        self._remote_control.execute_deactivate_magnet(callback)

    def execute_discharge_magnet(self, callback: CommandCallback) -> None:
        self._remote_control.execute_discharge_magnet(callback)

    def execute_update_directions(self, callback: CommandCallback) -> None:
        self._remote_control.execute_update_directions(callback)

    def execute_championship(self, callback: CommandCallback) -> None:
        self._remote_control.execute_championship(callback)

    def execute_look_down(self, callback: CommandCallback) -> None:
        self._remote_control.execute_look_down(callback)

    def execute_look_ahead(self, callback: CommandCallback) -> None:
        self._remote_control.execute_look_ahead(callback)
