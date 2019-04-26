from math import pi

from coordinate.absoluteCoordinate import AbsoluteCoordinate
from coordinate.orientation import Orientation
from cortex.domain.iAbsolutePathable import IAbsolutePathable
from cortex.domain.path.absoluteMovement import AbsoluteMovement
from cortex.domain.path.absolutePath import AbsolutePath
from cortex.domain.table import Table


class GrassfirePathable(IAbsolutePathable):
    angle_precision = pi / 4
    max_movement_length = 30

    def __init__(self, data: Table) -> None:
        self._table = data

    def path_from(self, position: AbsoluteCoordinate) -> AbsolutePath:
        previous_position = position
        current_position = self._get_grid_alignment(position)

        previous_movement = AbsoluteMovement(previous_position, current_position)
        # path_list = [previous_movement]
        path_list = []
        while self._table[current_position] != 0:
            current_position = self._get_adjacent_cell(current_position)
            current_movement = AbsoluteMovement(previous_position, current_position)
            if self._movement_follows_previous(current_movement, previous_movement) \
                    and previous_movement.length < self.max_movement_length:
                previous_movement.stop = current_movement.stop
            else:
                path_list.append(current_movement)
                previous_movement = current_movement
            previous_position = current_position

        if len(path_list) == 0:
            path_list.append(previous_movement)
        path_list[-1].stop.orientation = self._table.target_orientation
        return AbsolutePath(path_list)

    def _movement_follows_previous(self, movement: AbsoluteMovement, previous: AbsoluteMovement) -> bool:
        same_direction = movement.direction == previous.direction
        same_orientation = movement.stop.orientation == previous.stop.orientation
        return same_direction and same_orientation

    def _get_grid_alignment(self, position: AbsoluteCoordinate) -> AbsoluteCoordinate:
        orientation = position.orientation
        if orientation.radians % self.angle_precision <= self.angle_precision / 2:
            aligned_orientation = Orientation(orientation.radians // self.angle_precision * self.angle_precision)
        else:
            aligned_orientation = Orientation((orientation.radians // self.angle_precision + 1) * self.angle_precision)
        return AbsoluteCoordinate(position.x, position.y, aligned_orientation)

    def _get_adjacent_cell(self, cell: AbsoluteCoordinate) -> AbsoluteCoordinate:
        possible_cells = [
            AbsoluteCoordinate(cell.x, cell.y - 1, cell.orientation),  # North
            AbsoluteCoordinate(cell.x, cell.y + 1, cell.orientation),  # South
            AbsoluteCoordinate(cell.x + 1, cell.y, cell.orientation),  # East
            AbsoluteCoordinate(cell.x - 1, cell.y, cell.orientation),  # West
            AbsoluteCoordinate(cell.x + 1, cell.y - 1, cell.orientation),  # North-east
            AbsoluteCoordinate(cell.x - 1, cell.y + 1, cell.orientation),  # South-west
            AbsoluteCoordinate(cell.x + 1, cell.y + 1, cell.orientation),  # South-east
            AbsoluteCoordinate(cell.x - 1, cell.y - 1, cell.orientation)  # North-west
        ]

        for possible_cell in possible_cells:
            try:
                if self._table[possible_cell] < self._table[cell]:
                    return possible_cell
            except KeyError:
                pass
