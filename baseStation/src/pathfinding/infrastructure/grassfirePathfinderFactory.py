from typing import List

from pathfinding.domain.coord import Coord
from pathfinding.domain.iPathfinder import IPathfinder
from pathfinding.domain.iPathfinderFactory import IPathfinderFactory
from pathfinding.domain.table import Table
from pathfinding.infrastructure.grassfirePathfinder import GrassfirePathfinder


class GrassfirePathfinderFactory(IPathfinderFactory):
    def __init__(self, table_template: Table) -> None:
        self._table_template = table_template

    def create(self, obstacles: List[Coord]) -> IPathfinder:
        table = Table(self._table_template.height, self._table_template.width, self._table_template[Coord(0, 0)],
                      self._table_template.exclusion_radius, self._table_template.orientation,
                      self._table_template.border)
        return GrassfirePathfinder(table, obstacles)

    @property
    def exclusion_radius(self) -> float:
        return self._table_template.exclusion_radius

    @exclusion_radius.setter
    def exclusion_radius(self, value: float) -> None:
        self._table_template.exclusion_radius = value
