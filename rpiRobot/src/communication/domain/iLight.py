from abc import ABC, abstractmethod


class ILight(ABC):
    @property
    @abstractmethod
    def is_on(self) -> bool:
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass
