from typing import List

from application.domain.iObserver import IObserver
from prehensor.domain.prehensor import Prehensor


class PrehensorService:
    def __init__(self) -> None:
        self._prehensor: Prehensor = None
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update()

    def update_prehensor(self, prehensor: Prehensor) -> None:
        self._prehensor = prehensor
        self._notify()

    def get_prehensor(self) -> Prehensor:
        return self._prehensor
