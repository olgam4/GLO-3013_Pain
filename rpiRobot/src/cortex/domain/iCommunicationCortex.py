from abc import ABC, abstractmethod


class ICommunicationCortex(ABC):
    @abstractmethod
    def announce_win(self) -> None:
        pass
