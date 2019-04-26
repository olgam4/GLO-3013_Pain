from json import JSONDecodeError
from logging import getLogger

from communication.domain.iConnection import IConnection
from communication.domain.iRobotConnector import IRobotConnector
from communication.service.message import Message

logger = getLogger(__name__)


class CommunicationService:
    def __init__(self, robot_connector: IRobotConnector) -> None:
        self._connection: IConnection = robot_connector.connect_robot()

    def receive_message(self) -> Message:
        while True:
            data = self._connection.recv_msg()
            try:
                return Message.deserialize(data)
            except JSONDecodeError:
                logger.error("failed deserializing message: {}".format(data))

    def send_message(self, message: Message) -> None:
        self._connection.send_msg(message.serialize())
