class VisionError(Exception):
    """Base class for exceptions from the vision module"""

    def __init__(self, message: str) -> None:
        self._message = message

    @property
    def message(self) -> str:
        return self._message
