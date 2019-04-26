from abc import ABC, abstractmethod

from cortex.domain.iAbsolutePathable import IAbsolutePathable
from cortex.domain.table import Table


class IPathableFactory(ABC):
    @abstractmethod
    def create_from(self, data: Table) -> IAbsolutePathable:
        pass
