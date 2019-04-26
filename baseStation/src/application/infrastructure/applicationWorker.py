from logging import getLogger
from threading import Event
from time import sleep, time

from application.domain.iApplicationWorker import IApplicationWorker
from timer.service.timeService import TimeService
from vision.domain.visionError import VisionError
from vision.service.visionService import VisionService

logger = getLogger(__name__)


class ApplicationWorker(IApplicationWorker):
    def __init__(self, vision_service: VisionService, time_service: TimeService) -> None:
        self._vision_service = vision_service
        self._time_service = time_service
        self._stopped = Event()

    def run(self) -> None:
        while not self._stopped.is_set():
            self._update()
            sleep(1)

    def stop(self) -> None:
        self._stopped.set()

    def _update(self) -> None:
        logger.info("update {}".format(time()))
        try:
            self._vision_service.update()
        except VisionError as e:
            logger.info(e.message)
        self._time_service.update()
