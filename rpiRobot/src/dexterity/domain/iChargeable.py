from abc import ABC, abstractmethod


class IChargeable(ABC):
    @abstractmethod
    def get_charge(self) -> float:
        pass
