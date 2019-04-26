from abc import ABC, abstractmethod


class IPrehensor(ABC):
    @abstractmethod
    def grab(self) -> None:
        pass

    @abstractmethod
    def let_go(self) -> None:
        pass

    @abstractmethod
    def discharge(self) -> None:
        pass
