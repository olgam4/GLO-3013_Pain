from abc import ABC, abstractmethod


class ICommandStateNotifier(ABC):
    @abstractmethod
    def completed(self, command: str) -> None:
        pass

    @abstractmethod
    def errored(self, command: str) -> None:
        pass

    @abstractmethod
    def cancelled(self, command: str) -> None:
        pass
