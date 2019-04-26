from pathfinding.domain.iPathableCatalog import IPathableCatalog
from pathfinding.domain.table import Table


class PathfindingService:
    def __init__(self, pathable_catalog: IPathableCatalog) -> None:
        self._pathable_catalog = pathable_catalog

    def get_home(self) -> Table:
        return self._pathable_catalog.home

    def get_charge_station(self) -> Table:
        return self._pathable_catalog.charge_station

    def get_qr_code(self) -> Table:
        return self._pathable_catalog.qr_code

    def get_goal(self) -> Table:
        return self._pathable_catalog.goal

    def get_source(self) -> Table:
        return self._pathable_catalog.source
