from abc import ABC, abstractmethod

from cortex.domain.path.absolutePath import AbsolutePath


class IPathableCommunicator(ABC):
    @abstractmethod
    def request_charge_station_pathable(self) -> None:
        pass

    @abstractmethod
    def request_qr_code_pathable(self) -> None:
        pass

    @abstractmethod
    def request_source_pathable(self) -> None:
        pass

    @abstractmethod
    def request_goal_pathable(self) -> None:
        pass

    @abstractmethod
    def request_home_pathable(self) -> None:
        pass

    @abstractmethod
    def send_full_path(self, path: AbsolutePath) -> None:
        pass
