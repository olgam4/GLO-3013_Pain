from datetime import time, datetime, timedelta

from timer.domain.iChronometer import IChronometer


class PythonChronometer(IChronometer):
    def __init__(self) -> None:
        self._running: bool = False
        self._stopped: bool = False
        self._start_time = datetime.now()
        self._stop_time = self._start_time

    def start(self) -> None:
        if not self._running:
            self._running = True
            self._stopped = False
            self._start_time = datetime.now()

    def stop(self) -> None:
        if self._running:
            self._stopped = True
            self._stop_time = datetime.now()

    def reset(self) -> None:
        self._running = False
        self._stopped = True

    def get_current_time(self) -> float:
        return self._get_chronometer_time().seconds

    def _get_chronometer_time(self) -> timedelta:
        if not self._running:
            return timedelta(0)
        elif self._stopped:
            return self._stop_time - self._start_time
        else:
            return datetime.now() - self._start_time
