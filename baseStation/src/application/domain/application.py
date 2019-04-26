from threading import Thread

from application.domain.iApplicationWorker import IApplicationWorker
from application.domain.iChargeStationWatcher import IChargeStationWatcher
from application.domain.iRobotWatcher import IRobotWatcher
from application.domain.iUi import IUi


class Application:
    def __init__(self, ui: IUi, robot_watcher: IRobotWatcher, application_worker: IApplicationWorker,
                 charge_station_watcher: IChargeStationWatcher):
        self._ui: IUi = ui
        self._robot_watcher: IRobotWatcher = robot_watcher
        self._robot_watcher_thread = Thread(target=self._robot_watcher.run)
        self._application_worker = application_worker
        self._application_worker_thread = Thread(target=self._application_worker.run)
        self._charge_station_watcher = charge_station_watcher
        self._charge_station_watcher_thread = Thread(target=self._charge_station_watcher.run)

    def run(self) -> None:
        self._robot_watcher_thread.start()
        self._application_worker_thread.start()
        self._charge_station_watcher_thread.start()
        self._ui.run()

        self._stop()

    def _stop(self) -> None:
        self._robot_watcher.stop()
        self._application_worker.stop()
        self._charge_station_watcher.stop()
        self._robot_watcher_thread.join()
        self._application_worker_thread.join()
        self._charge_station_watcher_thread.join()
