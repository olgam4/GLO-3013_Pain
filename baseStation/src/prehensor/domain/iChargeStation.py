from abc import ABC, abstractmethod


class IChargeStation(ABC):
    @abstractmethod
    def recv(self) -> str:
        pass
