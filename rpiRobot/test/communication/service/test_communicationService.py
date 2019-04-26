from unittest import TestCase
from unittest.mock import Mock

from communication.service.communicationService import CommunicationService
from communication.service.message import Message


class TestCommunicationService(TestCase):
    def setUp(self) -> None:
        self.base_connector = Mock()
        self.connection = Mock()
        self.base_connector.connect_base.return_value = self.connection
        self.test_message = Message("test_message", variable1="variable1")

    def test_when_created_then_creates_a_socket_from_connector(self) -> None:
        CommunicationService(self.base_connector)

        self.assertTrue(self.base_connector.connect_base.called)

    def test_when_send_message_then_message_is_sent_on_socket(self) -> None:
        communication_service = CommunicationService(self.base_connector)

        communication_service.send_message(self.test_message)

        self.assertTrue(self.connection.send_msg.called)

    def test_when_receive_message_then_message_is_correct(self) -> None:
        message_data = self.test_message.serialize()
        self.connection.recv_msg.return_value = message_data
        communication_service = CommunicationService(self.base_connector)

        received_message = communication_service.receive_message()

        self.assertEqual(self.test_message, received_message)
