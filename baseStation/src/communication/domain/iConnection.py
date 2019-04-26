from abc import ABC, abstractmethod


class IConnection(ABC):
    @abstractmethod
    def send_msg(self, data: str) -> None:
        pass

    @abstractmethod
    def recv_msg(self) -> str:
        pass
