from mobility.domain.operation.operation import Operation
from mobility.service.mobilityService import MobilityService


class RemoteService:
    def __init__(self, mobility_service: MobilityService) -> None:
        self._mobility_service = mobility_service

    def execute_operation(self, operation: Operation) -> None:
        self._mobility_service.operate([operation])
