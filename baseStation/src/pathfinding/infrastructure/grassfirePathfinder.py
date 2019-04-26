from queue import Queue
from typing import List

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord
from pathfinding.domain.iPathfinder import IPathfinder
from pathfinding.domain.pathfindingError import CannotPathThereError
from pathfinding.domain.position import Position
from pathfinding.domain.table import Table


class GrassfirePathfinder(IPathfinder):
    def __init__(self, template_table: Table, obstacles: List[Coord]) -> None:
        self._obstacle_table = template_table
        self._fill_obstacle_table(obstacles)

    def pathable_to(self, position: Position) -> Table:
        approach_coordinate: Coord = position.coordinate
        pathable = self._obstacle_table.clone()
        pathable.orientation = position.orientation
        if pathable[approach_coordinate] == float('inf'):
            raise CannotPathThereError
        pathable[approach_coordinate] = 0
        next_cells = Queue()
        next_cells.put(approach_coordinate)

        while not next_cells.empty():
            current_cell = next_cells.get()
            adjacent_cells = self._get_adjacent_cells(current_cell, pathable)
            for cell in adjacent_cells:
                pathable[cell] = pathable[current_cell] + 1
                next_cells.put(cell)
        return pathable

    def _fill_obstacle_table(self, obstacles_centers: List[Coord]) -> None:
        for obstacle in obstacles_centers:
            self._obstacle_table.add_obstacle(obstacle)
        self._add_border_to_obstacle_table()

    def _add_border_to_obstacle_table(self) -> None:
        for x in range(self._obstacle_table.width):
            for y in range(self._obstacle_table.height):
                cell = Coord(x, y)
                if cell.x < self._obstacle_table.border or cell.x > self._obstacle_table.width\
                        - self._obstacle_table.border - 1:
                    self._obstacle_table[cell] = float("inf")
                if cell.y < self._obstacle_table.border or cell.y > self._obstacle_table.height\
                        - self._obstacle_table.border - 1:
                    self._obstacle_table[cell] = float("inf")

    def _get_adjacent_cells(self, cell: Coord, table: Table) -> List[Coord]:
        possible_cells = [
            Coord(cell.x, cell.y - 1),
            Coord(cell.x + 1, cell.y - 1),
            Coord(cell.x + 1, cell.y),
            Coord(cell.x + 1, cell.y + 1),
            Coord(cell.x, cell.y + 1),
            Coord(cell.x - 1, cell.y + 1),
            Coord(cell.x - 1, cell.y),
            Coord(cell.x - 1, cell.y - 1)
        ]

        valid_cells = []
        for possible_cell in possible_cells:
            try:
                if table[possible_cell] < 0:
                    valid_cells.append(possible_cell)
            except KeyError:
                pass

        return valid_cells


if __name__ == '__main__':
    template_table = Table(30, 30, -1, 7, Angle(0), 1)
    obstacles = [Coord(14, 14)]
    grassfire_pathfinder = GrassfirePathfinder(template_table, obstacles)
    dest_map = grassfire_pathfinder.pathable_to(Position(Coord(20, 20), Angle(0)))
    print(dest_map)
