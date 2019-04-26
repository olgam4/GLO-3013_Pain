from math import pi
from unittest import TestCase

from coordinate.absoluteCoordinate import AbsoluteCoordinate
from coordinate.orientation import Orientation
from cortex.domain.path.absoluteMovement import AbsoluteMovement
from cortex.domain.path.absolutePath import AbsolutePath
from cortex.domain.table import Table
from cortex.infrastructure.pathableGrassfire import GrassfirePathable

SOME_TABLE_WHICH_GOAL_IS_9_9 = Table(10, 10,
                                     [11.0, 10.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 11.0, 10.0, 9.0, 8.0,
                                      8.0, 8.0, 8.0, 8.0, 8.0, 9.0, 11.0, 10.0, 9.0, 8.0, 7.0, 7.0, 7.0, 7.0,
                                      float("inf"), float("inf"), 10.0, 10.0, float("inf"), float("inf"),
                                      float("inf"), 6.0, 6.0, 6.0, float("inf"), float("inf"), 9.0, 9.0,
                                      float("inf"), float("inf"), float("inf"), 5.0, 5.0, 5.0, float("inf"),
                                      float("inf"), 9.0, 8.0, float("inf"), float("inf"), float("inf"), 4.0,
                                      4.0,
                                      4.0, 4.0, 4.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 3.0, 3.0, 3.0, 9.0, 8.0,
                                      7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 2.0, 2.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0,
                                      2.0, 1.0, 1.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0],
                                     Orientation(pi / 2))

SOME_TABLE_WHICH_GOAL_IS_0_0 = Table(10, 10,
                                     [0, float("inf"), float("inf"), float("inf"), 8.0, 8.0, 8.0, 9.0, 10.0, 11.0,
                                      1.0, float("inf"), float("inf"), float("inf"), 7.0, 7.0, 8.0, 9.0, 10.0, 11.0,
                                      2.0, float("inf"), float("inf"), float("inf"), 6.0, 7.0, 8.0, 9.0, 10.0, 11.0,
                                      3.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0,
                                      4.0, 4.0, 4.0, 5.0, 6.0, float("inf"), float("inf"), float("inf"), 10.0, 11.0,
                                      5.0, 5.0, 5.0, 5.0, 6.0, float("inf"), float("inf"), float("inf"), 11.0, 11.0,
                                      6.0, 6.0, 6.0, 6.0, 6.0, float("inf"), float("inf"), float("inf"), 10.0, 11.0,
                                      7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 8.0, 9.0, 10.0, 11.0,
                                      8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 9.0, 10.0, 11.0,
                                      9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 10.0, 11.0],
                                     Orientation(0))

POSITION_0_0 = AbsoluteCoordinate(0.0, 0.0, Orientation(0))

POSITION_2_2 = AbsoluteCoordinate(2.0, 2.0, Orientation(0))

POSITION_9_9 = AbsoluteCoordinate(9.0, 9.0, Orientation(pi / 2))


class TestPathableGrassfire(TestCase):
    def test_when_path_from_some_point_then_last_position_is_correct_one(self) -> None:
        self.grassfire_pathable_9_9 = GrassfirePathable(SOME_TABLE_WHICH_GOAL_IS_9_9)

        path = self.grassfire_pathable_9_9.path_from(POSITION_2_2)

        self.assertEqual(POSITION_9_9, path.movements[-1].stop)

    def test_when_path_from_some_other_point_then_last_position_is_correct_one(self) -> None:
        self.grassfire_pathable_0_0 = GrassfirePathable(SOME_TABLE_WHICH_GOAL_IS_0_0)
        path = self.grassfire_pathable_0_0.path_from(POSITION_9_9)

        self.assertEqual(POSITION_0_0, path.movements[-1].stop)

    def test_whenPathingFromUnalignedPositionClosestToLowerAngle_thenRotationAlignsToLowerAngle(self) -> None:
        self.grassfire_pathable_0_0 = GrassfirePathable(SOME_TABLE_WHICH_GOAL_IS_0_0)
        unaligned_position = AbsoluteCoordinate(1, 3, Orientation(5 * pi / 16))

        path = self.grassfire_pathable_0_0.path_from(unaligned_position)

        self.assertEqual(Orientation(pi / 4), path.movements[0].stop.orientation)

    def test_whenPathingFromUnalignedPositionClosestToUpperAngle_thenRotationAlignsToUpperAngle(self) -> None:
        self.grassfire_pathable_0_0 = GrassfirePathable(SOME_TABLE_WHICH_GOAL_IS_0_0)
        unaligned_position = AbsoluteCoordinate(1, 3, Orientation(7 * pi / 16))

        path = self.grassfire_pathable_0_0.path_from(unaligned_position)

        self.assertEqual(Orientation(pi / 2), path.movements[0].stop.orientation)

    def test_whenPathingFromUnalignedPositionClosestToAngle_thenRotationAlignsToAngle(self) -> None:
        self.grassfire_pathable_0_0 = GrassfirePathable(SOME_TABLE_WHICH_GOAL_IS_0_0)
        unaligned_position = AbsoluteCoordinate(1, 3, Orientation(15 * pi / 16))

        path = self.grassfire_pathable_0_0.path_from(unaligned_position)

        self.assertEqual(Orientation(pi), path.movements[0].stop.orientation)

    def test_whenPathingFromSpecificPosition_thenPathIsRight(self) -> None:
        self.grassfire_pathable_0_0 = GrassfirePathable(SOME_TABLE_WHICH_GOAL_IS_0_0)
        unaligned_position = AbsoluteCoordinate(1, 3, Orientation(15 * pi / 16))

        path = self.grassfire_pathable_0_0.path_from(unaligned_position)

        expected_path = AbsolutePath([
            AbsoluteMovement(unaligned_position, AbsoluteCoordinate(0, 2, Orientation(pi))),
            AbsoluteMovement(AbsoluteCoordinate(0, 2, Orientation(pi)), AbsoluteCoordinate(0, 0, Orientation(0)))])
        self.assertEqual(expected_path, path)
