from abc import ABC, abstractmethod


class IEyes(ABC):
    @abstractmethod
    def look_ahead(self) -> None:
        pass

    @abstractmethod
    def look_down(self) -> None:
        pass
