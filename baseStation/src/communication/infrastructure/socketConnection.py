import struct
from socket import socket, timeout
from threading import Lock

from communication.domain.iConnection import IConnection


class SocketConnection(IConnection):
    def __init__(self, sock: socket) -> None:
        self._socket = sock
        self._send_lock = Lock()

    def send_msg(self, data: str) -> None:
        message = data.encode()
        with self._send_lock:
            self._socket.sendall(struct.pack('!I', len(message)))
            self._socket.sendall(message)

    def recv_msg(self) -> str:
        try:
            length, = struct.unpack('!I', self._recvall(4))
            return self._recvall(length).decode()
        except timeout:
            raise TimeoutError()

    def _recvall(self, count: int) -> bytes:
        buf = b""
        while count > 0:
            newbuf = self._socket.recv(count)
            if not newbuf:
                raise TimeoutError()
            buf += newbuf
            count -= len(newbuf)
        return buf
