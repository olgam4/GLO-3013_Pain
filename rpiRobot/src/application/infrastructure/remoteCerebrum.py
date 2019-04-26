from logging import getLogger
from threading import Event
from time import sleep

from application.domain.iCerebrum import ICerebrum

logger = getLogger(__name__)


class RemoteCerebrum(ICerebrum):
    def __init__(self) -> None:
        self._stopped = Event()

    def run(self) -> None:
        while not self._stopped.is_set():
            sleep(10)
            logger.info("doing nothing.")

    def stop(self) -> None:
        self._stopped.set()
