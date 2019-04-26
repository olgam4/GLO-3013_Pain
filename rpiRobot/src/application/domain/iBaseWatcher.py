from abc import ABC, abstractmethod


class IBaseWatcher(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
