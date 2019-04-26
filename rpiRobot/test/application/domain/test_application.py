from unittest import TestCase
from unittest.mock import Mock

from application.domain.application import Application


class TestApplication(TestCase):
    def setUp(self) -> None:
        self.cerebrum = Mock()
        self.robot_worker = Mock()
        self.base_watcher = Mock()
        self.application = Application(cerebrum=self.cerebrum, robot_worker=self.robot_worker,
                                       base_watcher=self.base_watcher)

    def test_when_running_the_application_then_the_parts_are_run(self) -> None:
        self.application.run()

        self.assertTrue(self.cerebrum.run.called)
        self.assertTrue(self.robot_worker.run.called)
        self.assertTrue(self.base_watcher.run.called)
