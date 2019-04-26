import struct
from unittest import TestCase
from unittest.mock import Mock, call

from communication.infrastructure.socketConnection import SocketConnection


class TestSocketConnection(TestCase):
    test_message = "this is a test message"

    def setUp(self) -> None:
        self.socket = Mock()
        self.socket_connection = SocketConnection(self.socket)

    def test_when_sending_a_message_then_message_length_and_encoding_is_sent_on_socket(self) -> None:
        self.socket_connection.send_msg(self.test_message)

        calls = self.socket.method_calls
        message_data = self.test_message.encode()
        expected_calls = [call.sendall(struct.pack('!I', len(message_data))), call.sendall(message_data)]
        self.assertListEqual(expected_calls, calls)

    def test_when_receiving_a_message_then_proper_message_is_received(self) -> None:
        message_data = self.test_message.encode()
        self.socket.recv.side_effect = [struct.pack('!I', len(message_data)), message_data]

        message = self.socket_connection.recv_msg()

        self.assertEqual(self.test_message, message)

    def test_when_receiving_a_message_then_message_length_and_encoding_is_received(self) -> None:
        message_data = self.test_message.encode()
        self.socket.recv.side_effect = [struct.pack('!I', len(message_data)), message_data]

        self.socket_connection.recv_msg()

        calls = self.socket.method_calls
        expected_calls = [call.recv(4), call.recv(len(message_data))]
        self.assertListEqual(expected_calls, calls)
