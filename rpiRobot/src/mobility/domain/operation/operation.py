from abc import ABC, abstractmethod

from mobility.domain.iDrivable import IDrivable


class Operation(ABC):
    @abstractmethod
    def execute(self, drivable: IDrivable) -> None:
        pass
