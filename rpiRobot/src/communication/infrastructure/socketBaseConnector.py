from logging import getLogger
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from typing import Tuple

from communication.domain.iBaseConnector import IBaseConnector
from communication.domain.iConnection import IConnection
from communication.infrastructure.socketConnection import SocketConnection

Address = Tuple[str, int]

logger = getLogger(__name__)


class SocketBaseConnector(IBaseConnector):
    def __init__(self, port: int) -> None:
        self._port = port

    def connect_base(self) -> IConnection:
        msg = ''
        address = ('', 0)
        while not msg == "request pain\n":
            msg, address = self._receive_broadcast()
            msg = msg.decode()
            logger.debug("connection request: {}".format(msg))
            logger.debug("received from {}".format(str(address)))
        address = (address[0], self._port)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(address)
        return SocketConnection(s)

    def _receive_broadcast(self) -> Tuple[bytes, Address]:
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', self._port))
        return s.recvfrom(1024)
