from logging import getLogger, Logger
from time import sleep

from communication.domain.iConnection import IConnection

logger: Logger = getLogger(__name__)


class NullConnection(IConnection):
    def send_msg(self, data: str) -> None:
        pass

    def recv_msg(self) -> str:
        sleep(10)
        logger.info("doing nothing")
        raise TimeoutError()
        return ""
