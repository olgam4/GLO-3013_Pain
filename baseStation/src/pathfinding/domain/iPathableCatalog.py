from abc import ABC, abstractmethod

from pathfinding.domain.table import Table


class IPathableCatalog(ABC):
    @property
    @abstractmethod
    def home(self) -> Table:
        pass

    @property
    @abstractmethod
    def charge_station(self) -> Table:
        pass

    @property
    @abstractmethod
    def qr_code(self) -> Table:
        pass

    @property
    @abstractmethod
    def goal(self) -> Table:
        pass

    @property
    @abstractmethod
    def source(self) -> Table:
        pass
