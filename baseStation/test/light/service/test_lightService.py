from unittest import TestCase
from unittest.mock import Mock

from light.domain.light import Light
from light.service.lightService import LightService


class TestLightService(TestCase):
    def setUp(self) -> None:
        self.observer = Mock()
        self.service = LightService()

    def test_given_an_observer_when_service_updated_then_observer_is_updated(self) -> None:
        self.service.attach(self.observer)
        new_light = Light(True)

        self.service.update_light(new_light)

        self.observer.update.assert_called_once()

    def test_given_updated_service_with_light_on_when_getting_light_then_lightDTO_has_on_state(self) -> None:
        light_on = Light(True)
        self.service.update_light(light_on)

        light_dto = self.service.get_light()

        self.assertTrue(light_dto.is_on)

    def test_given_updated_service_with_light_off_when_getting_light_then_lightDTO_has_off_state(self) -> None:
        light_on = Light(False)
        self.service.update_light(light_on)

        light_dto = self.service.get_light()

        self.assertFalse(light_dto.is_on)
