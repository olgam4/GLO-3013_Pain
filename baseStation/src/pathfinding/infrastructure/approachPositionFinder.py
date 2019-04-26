from pathfinding.domain.coord import Coord
from pathfinding.domain.iApproachPositionFinder import IApproachPositionFinder
from pathfinding.domain.position import Position

TABLE_WIDTH = 231
TABLE_HEIGHT = 111
EXCLUSION_BORDER = 30


class ApproachPositionFinder(IApproachPositionFinder):
    def calculate_from(self, position: Position) -> Position:
        x, y = position.coordinate.x, position.coordinate.y
        if x < EXCLUSION_BORDER:
            x = EXCLUSION_BORDER
        if x > TABLE_WIDTH - EXCLUSION_BORDER:
            x = TABLE_WIDTH - EXCLUSION_BORDER
        if y < EXCLUSION_BORDER:
            y = EXCLUSION_BORDER
        if y > TABLE_HEIGHT - EXCLUSION_BORDER:
            y = TABLE_HEIGHT - EXCLUSION_BORDER
        return Position(Coord(int(x), int(y)), position.orientation)
