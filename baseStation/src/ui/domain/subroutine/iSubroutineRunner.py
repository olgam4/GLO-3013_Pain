from abc import ABC, abstractmethod

from remote.domain.commandCallback import CommandCallback


class ISubroutineRunner(ABC):
    @abstractmethod
    def execute_charge_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_go_home_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_read_qr_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_grab_subroutine(self, target: str, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_drop_subroutine(self, target: str, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_switch_light_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_directional_movement(self, direction: str, speed: str, distance: float,
                                     callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_rotational_movement(self, angle: float, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_activate_magnet(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_deactivate_magnet(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_update_directions_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_discharge_magnet(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_championship_subroutine(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_look_down(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass

    @abstractmethod
    def execute_look_ahead(self, callback: CommandCallback) -> None:
        """

        :raises BlockingIOError: command already running
        """
        pass
