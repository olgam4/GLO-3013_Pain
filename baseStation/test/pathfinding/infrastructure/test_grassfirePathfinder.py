from unittest import TestCase

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord
from pathfinding.domain.position import Position
from pathfinding.domain.table import Table
from pathfinding.infrastructure.grassfirePathfinder import GrassfirePathfinder

EXPECTED_PATH = [float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"),
                 float("inf"), 29, 29, 29, 28, 27, 26, 25, 24, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,
                 23, 23, 23, 23, 23, 23, float("inf"),
                 float("inf"), 28, 28, 28, 28, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 22,
                 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, float("inf"),
                 float("inf"), 27, 27, 27, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
                 float("inf"),
                 float("inf"), 26, 26, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                 20, 20, 20, 20, 20, float("inf"),
                 float("inf"), 25, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), 20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
                 19, 19, 19, 19, 19, float("inf"),
                 float("inf"), 24, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), 20, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
                 18, 18, 18, 18, 18, float("inf"),
                 float("inf"), 23, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), 20, 19, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17,
                 17, 17, 17, 17, 17, float("inf"),
                 float("inf"), 23, 22, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), 20, 19, 18, 17, 16, 16, 16, 16, 16, 16, 16, 16,
                 16, 16, 16, 16, 16, float("inf"),
                 float("inf"), 23, 22, 21, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), 21, 20, 19, 18, 17, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
                 float("inf"),
                 float("inf"), 23, 22, 21, 20, float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 20,
                 20, 20, 19, 18, 17, 16, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, float("inf"), float("inf"), float("inf"), 19, 19, 19, 19, 19, 18, 17,
                 16, 15, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), 12, 12, 12, 12, 12, 12, 12, 12, 12, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 17, 17, 17, 17, 17, 17, float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 11, 11, 11, 11, 11, 11, 11, 11,
                 float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 16, 16, 16, 16, float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 10, 10, 10, 10, 10,
                 10, 10, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 15, 15, float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 9, 9,
                 9, 9, 9, 9, 9, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 14, float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 8, 8,
                 8, 8, 8, 8, 8, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 7, 7,
                 7, 7, 7, 7, 7, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 6, 6, 6, 6, 6, 6,
                 6, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), 5, 5, 5, 5, 5, 5, 5, 5,
                 float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), 4, 4, 4, 4, 4, 4, 4, 4, 4, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, float("inf"), float("inf"),
                 float("inf"), 5, 4, 3, 3, 3, 3, 3, 3, 3, 4, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 2, 2, 2,
                 2, 3, 4, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1,
                 2, 3, 4, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 1,
                 2, 3, 4, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1,
                 2, 3, 4, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 2, 2, 2,
                 2, 3, 4, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 3, 3, 3, 3,
                 3, 3, 4, float("inf"),
                 float("inf"), 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 4, 4, 4, 4, 4,
                 4, 4, 4, float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"),
                 float("inf"), float("inf")]


class TestGrassfirePathfinder(TestCase):
    def setUp(self) -> None:
        table = Table(30, 30, -1, 5, Angle(0), 1)
        self.grassfire_pathfinder = GrassfirePathfinder(table, [Coord(7, 7), Coord(17, 17)])

    def test_when_pathing_to_some_point_then_gives_the_right_map(self) -> None:
        path = self.grassfire_pathfinder.pathable_to(Position(Coord(24, 24), Angle(0)))
        self.assertEqual(path.data, EXPECTED_PATH)
