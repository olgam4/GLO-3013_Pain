from abc import ABC, abstractmethod

from coordinate.absoluteCoordinate import AbsoluteCoordinate
from cortex.domain.path.absolutePath import AbsolutePath


class IAbsolutePathable(ABC):
    @abstractmethod
    def path_from(self, position: AbsoluteCoordinate) -> AbsolutePath:
        pass
