from abc import ABC, abstractmethod


class INapCortex(ABC):
    @abstractmethod
    def recharge(self) -> None:
        pass
