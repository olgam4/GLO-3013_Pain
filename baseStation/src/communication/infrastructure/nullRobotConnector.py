from communication.domain.iConnection import IConnection
from communication.domain.iRobotConnector import IRobotConnector
from communication.infrastructure.nullConnection import NullConnection


class NullRobotConnector(IRobotConnector):
    def connect_robot(self) -> IConnection:
        return NullConnection()
