from typing import List

from light.domain.light import Light
from light.service.lightDTO import LightDTO
from application.domain.iObserver import IObserver


class LightService:
    def __init__(self) -> None:
        self._light: Light = None
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update()

    def update_light(self, light: Light) -> None:
        self._light = light
        self._notify()

    def get_light(self) -> LightDTO:
        return LightDTO(self._light.is_on)
