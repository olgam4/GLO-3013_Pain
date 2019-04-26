class LightDTO:
    def __init__(self, turned_on: bool):
        self._turned_on = turned_on

    @property
    def is_on(self) -> bool:
        return self._turned_on
