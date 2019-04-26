from communication.domain.iLight import ILight


class DisplayService:
    def __init__(self, light: ILight):
        self._light = light

    def switch_light(self) -> None:
        if self._light.is_on:
            self._light.turn_off()
        else:
            self._light.turn_on()

    def set_light_on(self)->None:
        self._light.turn_on()

    def set_light_off(self)->None:
        self._light.turn_off()

    def is_light_on(self) -> bool:
        return self._light.is_on
