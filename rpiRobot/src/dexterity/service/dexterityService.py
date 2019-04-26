from dexterity.domain.iPrehensor import IPrehensor


class DexterityService:
    def __init__(self, prehensor: IPrehensor):
        self._prehensor = prehensor

    def grab(self) -> None:
        self._prehensor.grab()

    def let_go(self) -> None:
        self._prehensor.let_go()

    def discharge(self) -> None:
        self._prehensor.discharge()
