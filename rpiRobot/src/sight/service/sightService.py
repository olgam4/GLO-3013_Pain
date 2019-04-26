from sight.domain.iEyes import IEyes


class SightService:
    def __init__(self, eyes: IEyes):
        self._eyes = eyes

    def look_ahead(self) -> None:
        with self._eyes:
            self._eyes.look_ahead()

    def look_down(self) -> None:
        with self._eyes:
            self._eyes.look_down()
