from _socket import SOCK_STREAM, SOCK_DGRAM
from unittest import TestCase
from unittest.mock import patch, Mock

from communication.infrastructure.socketBaseConnector import SocketBaseConnector


class TestSocketBaseConnector(TestCase):
    def setUp(self) -> None:
        socket_patcher = patch('communication.infrastructure.socketBaseConnector.socket')
        self.Socket = socket_patcher.start()
        self.addCleanup(socket_patcher.stop)

        self.port = 7347
        self.address = 'localhost'

        self.broadcast_socket = Mock()
        self.broadcast_socket.recvfrom.return_value = b'request pain\n', (self.address, 0)
        self.connection_socket = Mock()

        self.Socket.side_effect = self.mock_return

        self.base_connector = SocketBaseConnector(self.port)

    def mock_return(self, s_family: int, s_type: int) -> Mock:
        if s_type == SOCK_STREAM:
            return self.connection_socket
        elif s_type == SOCK_DGRAM:
            return self.broadcast_socket

    def test_when_connect_base_then_broadcast_listen_on_port(self) -> None:
        self.base_connector.connect_base()

        self.broadcast_socket.bind.assert_called_with(('', self.port))

    def test_when_connect_base_then_broadcast_received(self) -> None:
        self.base_connector.connect_base()

        self.assertTrue(self.broadcast_socket.recvfrom.called)

    def test_when_connect_base_then_connection_connects_address(self) -> None:
        self.base_connector.connect_base()

        self.connection_socket.connect.assert_called_with((self.address, self.port))
