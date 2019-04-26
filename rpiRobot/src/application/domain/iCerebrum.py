from abc import ABC, abstractmethod


class ICerebrum(ABC):
    @abstractmethod
    def run(self) -> None:
        pass
