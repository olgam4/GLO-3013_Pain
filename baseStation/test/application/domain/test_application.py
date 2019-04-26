from unittest import TestCase
from unittest.mock import Mock

from application.domain.application import Application


class TestApplication(TestCase):
    def setUp(self) -> None:
        self.ui = Mock()
        self.robot_watcher = Mock()
        self.application_worker = Mock()
        self.charge_station_watcher = Mock()
        self.application = Application(self.ui, self.robot_watcher, self.application_worker,
                                       self.charge_station_watcher)

    def test_when_running_the_application_then_the_parts_are_run(self) -> None:
        self.application.run()

        self.ui.run.assert_called()
        self.robot_watcher.run.assert_called()
        self.application_worker.run.assert_called()
        self.charge_station_watcher.run.assert_called()
