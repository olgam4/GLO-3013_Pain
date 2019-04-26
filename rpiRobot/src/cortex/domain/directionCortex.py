from communication.service.positionService import PositionService
from cortex.domain.path.absolutePath import AbsolutePath
from cortex.domain.pathableCatalog import PathableCatalog
from cortex.infrastructure.pathableCommunicator import PathableCommunicator
from mobility.service.mobilityService import MobilityService


class DirectionCortex:
    def __init__(self, pathable_catalog: PathableCatalog, position_service: PositionService,
                 mobility_service: MobilityService, pathable_communicator: PathableCommunicator) -> None:
        self._pathable_catalog = pathable_catalog
        self._position_service = position_service
        self._mobility_service = mobility_service
        self._pathable_communicator = pathable_communicator

    def reach_charge(self) -> None:
        position = self._position_service.get_position()
        path = self._pathable_catalog.charge_station.path_from(position)
        self._mobility_service.drive(path)

    def reach_home(self) -> None:
        position = self._position_service.get_position()
        path = self._pathable_catalog.home.path_from(position)
        self._mobility_service.drive(path)

    def reach_qr_code(self) -> None:
        position = self._position_service.get_position()
        path = self._pathable_catalog.qr_code.path_from(position)
        self._mobility_service.drive(path)

    def reach_source(self) -> None:
        position = self._position_service.get_position()
        path = self._pathable_catalog.source.path_from(position)
        self._mobility_service.drive(path)

    def reach_goal(self) -> None:
        position = self._position_service.get_position()
        path = self._pathable_catalog.goal.path_from(position)
        self._mobility_service.drive(path)

    def update_directions(self, need_charge: bool = True) -> None:
        self._pathable_catalog.populate(asynchronous=False)
        position = self._position_service.get_position()

        path = AbsolutePath([])
        if need_charge:
            charge_station_path = self._pathable_catalog.charge_station.path_from(position)
            path += charge_station_path
            position = path.movements[-1].stop

        qr_code_path = self._pathable_catalog.qr_code.path_from(position)
        path += qr_code_path
        position = path.movements[-1].stop

        source_path = self._pathable_catalog.source.path_from(position)
        path += source_path
        position = path.movements[-1].stop

        goal_path = self._pathable_catalog.goal.path_from(position)
        path += goal_path
        position = path.movements[-1].stop

        home_path = self._pathable_catalog.home.path_from(position)
        path += home_path

        self._pathable_communicator.send_full_path(path)
