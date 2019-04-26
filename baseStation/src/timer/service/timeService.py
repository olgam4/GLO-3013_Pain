from typing import List

from timer.domain.iChronometer import IChronometer
from timer.service.timeDTO import TimeDTO
from application.domain.iObserver import IObserver


class TimeService:
    def __init__(self, chronometer: IChronometer) -> None:
        self._chronometer = chronometer
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update()

    def start(self) -> None:
        self._chronometer.start()
        self._notify()

    def stop(self) -> None:
        self._chronometer.stop()
        self._notify()

    def update(self) -> None:
        self._notify()

    def get_current_time(self) -> TimeDTO:
        return TimeDTO(self._chronometer.get_current_time())

    def reset(self) -> None:
        self._chronometer.reset()
        self._notify()
