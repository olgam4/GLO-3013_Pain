class Prehensor:
    def __init__(self, charge: float) -> None:
        self._charge = charge

    @property
    def charge(self) -> float:
        return self._charge
