from typing import Callable

from remote.domain.commandStatus import CommandStatus


class CommandCallback:
    def __init__(self, command: Callable[[CommandStatus], None]) -> None:
        self._command = command

    def __call__(self, status: CommandStatus) -> None:
        self._command(status)
