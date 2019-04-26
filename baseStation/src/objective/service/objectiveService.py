from typing import List

from objective.domain.objective import Objective
from objective.service.objectiveDTO import ObjectiveDTO
from application.domain.iObserver import IObserver


class ObjectiveService:
    def __init__(self) -> None:
        self._objective: Objective = None
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update()

    def update_objective(self, objective: Objective) -> None:
        self._objective = objective
        self._notify()

    def get_objective(self) -> ObjectiveDTO:
        return ObjectiveDTO(self._objective.value)
