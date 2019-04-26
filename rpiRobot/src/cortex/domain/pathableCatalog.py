from logging import getLogger
from threading import Event, Thread, Lock

from cortex.domain.iAbsolutePathable import IAbsolutePathable
from cortex.domain.iPathableCommunicator import IPathableCommunicator

logger = getLogger(__name__)


class PathableCatalog:
    def __init__(self, pathable_communicator: IPathableCommunicator) -> None:
        self._pathable_communicator = pathable_communicator

        self._populated = Event()
        self._populating = Lock()
        self._populate_thread = None

        self._got_charge_station = Event()
        self._got_qr_code = Event()
        self._got_source = Event()
        self._got_goal = Event()
        self._got_home = Event()

        self._charge_station = None
        self._qr_code = None
        self._source = None
        self._goal = None
        self._home = None

    @property
    def charge_station(self) -> IAbsolutePathable:
        self.populate(asynchronous=False)
        return self._charge_station

    @charge_station.setter
    def charge_station(self, charge_station: IAbsolutePathable) -> None:
        self._got_charge_station.set()
        self._charge_station = charge_station

    @property
    def qr_code(self) -> IAbsolutePathable:
        self.populate(asynchronous=False)
        return self._qr_code

    @qr_code.setter
    def qr_code(self, qr_code: IAbsolutePathable) -> None:
        self._got_qr_code.set()
        self._qr_code = qr_code

    @property
    def source(self) -> IAbsolutePathable:
        self.populate(asynchronous=False)
        return self._source

    @source.setter
    def source(self, source: IAbsolutePathable) -> None:
        self._got_source.set()
        self._source = source

    @property
    def goal(self) -> IAbsolutePathable:
        self.populate(asynchronous=False)
        return self._goal

    @goal.setter
    def goal(self, goal: IAbsolutePathable) -> None:
        self._got_goal.set()
        self._goal = goal

    @property
    def home(self) -> IAbsolutePathable:
        self.populate(asynchronous=False)
        return self._home

    @home.setter
    def home(self, home: IAbsolutePathable) -> None:
        self._got_home.set()
        self._home = home

    def populate(self, asynchronous=True) -> None:
        with self._populating:
            if self._populated.is_set():
                return

            self._populate_thread = Thread(target=self._populate)
            self._populate_thread.start()

            if not asynchronous:
                self._populate_thread.join()

    def _populate(self) -> None:
        if not self._got_charge_station.is_set():
            self._pathable_communicator.request_charge_station_pathable()
        self._got_charge_station.wait()
        if not self._got_qr_code.is_set():
            self._pathable_communicator.request_qr_code_pathable()
        self._got_qr_code.wait()
        if not self._got_home.is_set():
            self._pathable_communicator.request_home_pathable()
        self._got_home.wait()
        if not self._got_source.is_set():
            self._pathable_communicator.request_source_pathable()
        self._got_source.wait()
        if not self._got_goal.is_set():
            self._pathable_communicator.request_goal_pathable()
        self._got_goal.wait()
        self._populated.set()
