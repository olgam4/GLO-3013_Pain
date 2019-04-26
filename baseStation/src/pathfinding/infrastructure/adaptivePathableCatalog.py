from math import pi
from threading import Lock, Event
from typing import List

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord
from pathfinding.domain.iApproachPositionFinder import IApproachPositionFinder
from pathfinding.domain.iPathableCatalog import IPathableCatalog
from pathfinding.domain.iPathfinderFactory import IPathfinderFactory
from pathfinding.domain.pathfindingError import CannotPathThereError
from pathfinding.domain.position import Position
from pathfinding.domain.table import Table
from vision.domain.visionError import VisionError
from vision.service.visionService import VisionService


class AdaptivePathableCatalog(IPathableCatalog):
    charge_position_pos = Position(Coord(21, 80), Angle(0))
    qr_codes_pos = [Position(Coord(190, 40), Angle(pi)), Position(Coord(170, 60), Angle(7 * pi / 8))]
    home_pos = Position(Coord(55, 55), Angle(0))

    def __init__(self, vision_service: VisionService, pathfinder_factory: IPathfinderFactory,
                 approach_position_finder: IApproachPositionFinder) -> None:
        self._vision_service = vision_service
        self._pathfinder_factory = pathfinder_factory
        self._approach_position_finder = approach_position_finder

        self._populating = Lock()
        self._filled = Event()

    @property
    def home(self) -> Table:
        with self._populating:
            if not self._filled.is_set():
                self._fill()
            return self._home

    @property
    def charge_station(self) -> Table:
        with self._populating:
            if not self._filled.is_set():
                self._fill()
            return self.charge_station

    @property
    def qr_code(self) -> Table:
        with self._populating:
            if not self._filled.is_set():
                self._fill()
            return self._qr_code

    @property
    def goal(self) -> Table:
        with self._populating:
            if not self._filled.is_set():
                self._fill()
            return self._goal

    @property
    def source(self) -> Table:
        with self._populating:
            if not self._filled.is_set():
                self._fill()
            return self._source

    def _fill(self) -> None:
        obstacles = self._find_obstacles()
        self._find_destinations()

        pathfinder = self._pathfinder_factory.create(obstacles)
        while not self._filled.is_set():
            self._charge_station: Table = pathfinder.pathable_to(self.charge_position_pos)
            found_path = False
            for qr_code in self.qr_codes_pos:
                try:
                    self._qr_code = pathfinder.pathable_to(qr_code)
                    found_path = True
                except CannotPathThereError:
                    continue
            if not found_path:
                raise CannotPathThereError
            self._home: Table = pathfinder.pathable_to(self.home_pos)
            self._source: Table = pathfinder.pathable_to(self.source_pos)
            self._goal: Table = pathfinder.pathable_to(self.goal_pos)
            try:
                assert self._charge_station[self.home_pos.coordinate] != -1 and self._charge_station[
                    self.home_pos.coordinate] != float("inf")
                assert self._qr_code[self.home_pos.coordinate] != -1 and self._qr_code[
                    self.home_pos.coordinate] != float("inf")
                assert self._source[self.home_pos.coordinate] != -1 and self._source[
                    self.home_pos.coordinate] != float("inf")
                assert self._goal[self.home_pos.coordinate] != -1 and self._goal[
                    self.home_pos.coordinate] != float("inf")
                self._filled.set()
            except AssertionError:
                self._pathfinder_factory.exclusion_radius -= 1
                print(self._pathfinder_factory.exclusion_radius)
                pathfinder = self._pathfinder_factory.create(obstacles)

    def _find_obstacles(self) -> List[Coord]:
        found_obstacles = False
        count = 3
        obstacles = []
        while not found_obstacles and count > 0:
            try:
                self._vision_service.update()
                obstacles = [obstacle.to_centimeters() for obstacle in self._vision_service.get_obstacles()]
                found_obstacles = True
            except VisionError:
                count -= 1
        return obstacles

    def _find_destinations(self) -> None:
        source = self._vision_service.get_source()
        source = Position(source.coordinate.to_centimeters(), source.orientation)
        self.source_pos = self._approach_position_finder.calculate_from(source)

        goal = self._vision_service.get_goal()
        goal = Position(goal.coordinate.to_centimeters(), goal.orientation)
        self.goal_pos = self._approach_position_finder.calculate_from(goal)
