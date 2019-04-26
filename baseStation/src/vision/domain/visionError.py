class VisionError(Exception):
    """Base class for exceptions from the vision module"""

    def __init__(self, message: str) -> None:
        self._message = message

    @property
    def message(self) -> str:
        return self._message


class VisionFactoryError(VisionError):
    """Base class for when a vision factory could not create his target object"""

    def __init__(self, message: str) -> None:
        self._message = message

    @property
    def message(self) -> str:
        return self._message
