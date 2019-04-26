from cortex.domain.iAbsolutePathable import IAbsolutePathable
from cortex.domain.iPathableFactory import IPathableFactory
from cortex.domain.table import Table
from cortex.infrastructure.pathableGrassfire import GrassfirePathable


class PathableFactory(IPathableFactory):
    def create_from(self, data: str) -> IAbsolutePathable:
        return GrassfirePathable(Table.deserialize(data))
