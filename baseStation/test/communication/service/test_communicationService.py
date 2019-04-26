from unittest import TestCase
from unittest.mock import Mock

from communication.service.communicationService import CommunicationService
from communication.service.message import Message


class TestCommunicationService(TestCase):
    def setUp(self) -> None:
        self.robot_connector = Mock()
        self.connection = Mock()
        self.robot_connector.connect_robot.return_value = self.connection
        self.test_message = Message("test_message", variable1="variable1")

    def test_when_created_then_creates_a_socket_from_connector(self) -> None:
        CommunicationService(self.robot_connector)

        self.robot_connector.connect_robot.assert_called_once()

    def test_when_send_message_then_message_is_sent_on_socket(self) -> None:
        communication_service = CommunicationService(self.robot_connector)

        communication_service.send_message(self.test_message)

        self.connection.send_msg.assert_called_once()

    def test_when_receive_message_then_message_is_correct(self) -> None:
        message_data = self.test_message.serialize()
        self.connection.recv_msg.return_value = message_data
        communication_service = CommunicationService(self.robot_connector)

        received_message = communication_service.receive_message()

        self.assertEqual(self.test_message, received_message)
