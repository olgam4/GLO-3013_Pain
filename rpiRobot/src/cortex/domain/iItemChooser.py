from abc import ABC, abstractmethod
from typing import List

from cortex.domain.objective.item import Item
from cortex.domain.objective.objective import Objective


class IItemChooser(ABC):
    @abstractmethod
    def choose_from(self, objective: Objective, items: List[Item]) -> List[Item]:
        pass
