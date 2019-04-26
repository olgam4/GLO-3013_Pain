from logging import Logger, getLogger
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_BROADCAST
from threading import Thread, Event
from time import sleep

from communication.domain.iConnection import IConnection
from communication.domain.iRobotConnector import IRobotConnector
from communication.infrastructure.socketConnection import SocketConnection

logger: Logger = getLogger(__name__)


class SocketRobotConnector(IRobotConnector):
    def __init__(self, port: int, address: str, timeout: float) -> None:
        self._timeout = timeout
        self._port = port
        self._address = address
        self._done = Event()
        self._listening_socket = socket(AF_INET, SOCK_STREAM)
        self._broadcast_socket = socket(AF_INET, SOCK_DGRAM)

    def connect_robot(self) -> IConnection:
        thread = Thread(target=self._broadcast, daemon=True)

        with self._listening_socket:
            self._listening_socket.bind(('', self._port))
            self._listening_socket.listen(0)
            thread.start()
            conn, address = self._listening_socket.accept()

        self._done.set()
        thread.join()

        conn.settimeout(self._timeout)
        return SocketConnection(conn)

    def _broadcast(self) -> None:
        destination = (self._address, self._port)
        self._broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        message = "request pain\n".encode()
        count = 0
        with self._broadcast_socket:
            while not self._done.is_set():
                logger.info("broadcast %s", count)
                count += 1
                self._broadcast_socket.sendto(message, destination)
                sleep(1)


if __name__ == "__main__":
    connector = SocketRobotConnector(7347, '<broadcast>')
    connection = connector.connect_robot()
    logger.debug(connection.recv_msg())
    logger.debug(connection.recv_msg())
    logger.debug(connection.recv_msg())
