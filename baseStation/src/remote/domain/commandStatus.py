from enum import Enum


class CommandStatus(Enum):
    completed = 0
    cancelled = 1
    errored = 2
