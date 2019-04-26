class Light:
    def __init__(self, turned_on: bool) -> None:
        self._turned_on = turned_on

    @property
    def is_on(self) -> bool:
        return self._turned_on
