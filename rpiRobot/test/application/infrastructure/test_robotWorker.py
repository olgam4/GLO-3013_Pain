from threading import Thread
from unittest import TestCase
from unittest.mock import Mock

from application.infrastructure.robotWorker import RobotWorker


class TestRobotWorker(TestCase):
    def setUp(self) -> None:
        self.vision_service = Mock()
        self.communication_service = Mock()
        self.display_service = Mock()
        self.chargeable = Mock()
        self.robot_worker = RobotWorker(vision_service=self.vision_service,
                                        communication_service=self.communication_service,
                                        display_service=self.display_service,
                                        chargeable=self.chargeable)

    def test_when_stopped_then_is_stopped(self) -> None:
        thread = Thread(target=self.robot_worker.run)

        self.robot_worker.stop()

        thread.start()
        thread.join(timeout=1)
        self.assertFalse(thread.isAlive())

    def test_when_running_then_update_message_is_sent(self)->None:
        thread = Thread(target=self.robot_worker.run)
        self.robot_worker.PERIOD = 0

        thread.start()
        self.robot_worker.stop()
        thread.join(timeout=3)

        self.assertTrue(self.communication_service.send_message.called)
