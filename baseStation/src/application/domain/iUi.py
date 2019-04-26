from abc import ABC, abstractmethod


class IUi(ABC):
    @abstractmethod
    def run(self) -> None:
        pass
