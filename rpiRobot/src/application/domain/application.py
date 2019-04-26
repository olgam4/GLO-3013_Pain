from threading import Thread

from application.domain.iBaseWatcher import IBaseWatcher
from application.domain.iCerebrum import ICerebrum
from application.domain.iRobotWorker import IRobotWorker


class Application:
    def __init__(self, cerebrum: ICerebrum, robot_worker: IRobotWorker, base_watcher: IBaseWatcher):
        self._cerebrum = cerebrum
        self._robot_worker = robot_worker
        self._robot_worker_thread = Thread(target=self._robot_worker.run, daemon=True)
        self._base_watcher = base_watcher
        self._base_watcher_thread = Thread(target=self._base_watcher.run, daemon=True)

    def run(self) -> None:
        self._robot_worker_thread.start()
        self._base_watcher_thread.start()
        self._cerebrum.run()

        self._stop()

    def _stop(self) -> None:
        self._robot_worker.stop()
        self._base_watcher.stop()
        self._robot_worker_thread.join()
        self._base_watcher_thread.join()
