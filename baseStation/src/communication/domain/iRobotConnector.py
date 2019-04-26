from abc import ABC, abstractmethod

from communication.domain.iConnection import IConnection


class IRobotConnector(ABC):
    @abstractmethod
    def connect_robot(self) -> IConnection:
        pass
