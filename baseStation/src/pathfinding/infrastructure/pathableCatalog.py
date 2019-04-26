from logging import getLogger
from math import pi
from threading import Event, Lock

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord
from pathfinding.domain.iApproachPositionFinder import IApproachPositionFinder
from pathfinding.domain.iPathableCatalog import IPathableCatalog
from pathfinding.domain.iPathfinder import IPathfinder
from pathfinding.domain.iPathfinderFactory import IPathfinderFactory
from pathfinding.domain.pathfindingError import CannotPathThereError
from pathfinding.domain.position import Position
from pathfinding.domain.table import Table
from vision.domain.visionError import VisionError
from vision.infrastructure.cvVisionException import SourceCouldNotBeFound, GoalCouldNotBeFound
from vision.service.visionService import VisionService

logger = getLogger(__name__)


class PathableCatalog(IPathableCatalog):
    def __init__(self, vision_service: VisionService, pathfinder_factory: IPathfinderFactory,
                 approach_position_finder: IApproachPositionFinder) -> None:
        self._vision_service = vision_service
        self._pathfinder_factory = pathfinder_factory
        self._approach_position_finder = approach_position_finder
        self._pathfinder: IPathfinder = None

        self._populating = Lock()
        self._layout = Event()

        self._got_charge_station = Event()
        self._got_qr_code = Event()
        self._got_source = Event()
        self._got_goal = Event()
        self._got_home = Event()

        self._charge_station: Table = None
        self._qr_code: Table = None
        self._source: Table = None
        self._goal: Table = None
        self._home: Table = None

    @property
    def charge_station(self) -> Table:
        with self._populating:
            if not self._got_charge_station.is_set():
                self._set_layout()

                charge_station = Position(Coord(20, 80), Angle(0))
                self._charge_station = self._pathfinder.pathable_to(charge_station)

                self._got_charge_station.set()
        return self._charge_station

    @property
    def qr_code(self) -> Table:
        with self._populating:
            if not self._got_qr_code.is_set():
                self._set_layout()

                found_path = False
                for position in [Position(Coord(190, 40), Angle(pi)), Position(Coord(170, 60), Angle(7 * pi / 8))]:
                    try:
                        self._qr_code = self._pathfinder.pathable_to(position)
                        found_path = True
                    except CannotPathThereError:
                        continue
                if not found_path:
                    raise CannotPathThereError

                self._got_qr_code.set()
        return self._qr_code

    @property
    def source(self) -> Table:
        with self._populating:
            if not self._got_source.is_set():
                self._set_layout()

                for i in range(3):
                    try:
                        position = self._vision_service.get_source()
                        break
                    except SourceCouldNotBeFound:
                        logger.info("SourceCouldNotBeFound")
                source = Position(position.coordinate.to_centimeters(), position.orientation)
                approach_position = self._approach_position_finder.calculate_from(source)
                self._source = self._pathfinder.pathable_to(approach_position)

                self._got_source.set()
        return self._source

    @property
    def goal(self) -> Table:
        with self._populating:
            if not self._got_goal.is_set():
                self._set_layout()

                for i in range(3):
                    try:
                        position = self._vision_service.get_goal()
                        break
                    except GoalCouldNotBeFound:
                        logger.info("GoalCouldNotBeFound")
                goal = Position(position.coordinate.to_centimeters(), position.orientation)
                approach_position = self._approach_position_finder.calculate_from(goal)
                self._goal = self._pathfinder.pathable_to(approach_position)

                self._got_goal.set()
        return self._goal

    @property
    def home(self) -> Table:
        with self._populating:
            if not self._got_home.is_set():
                self._set_layout()

                home = Coord(55, 55)
                self._home = self._pathfinder.pathable_to(Position(home, Angle(0)))

                self._got_home.set()
        return self._home

    def _set_layout(self) -> None:
        if self._layout.is_set():
            return
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
        self._pathfinder = self._pathfinder_factory.create(obstacles)
        self._layout.set()
