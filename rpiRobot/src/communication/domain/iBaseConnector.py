from abc import ABC, abstractmethod

from communication.domain.iConnection import IConnection


class IBaseConnector(ABC):
    @abstractmethod
    def connect_base(self) -> IConnection:
        pass
