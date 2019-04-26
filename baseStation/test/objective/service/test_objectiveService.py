from unittest import TestCase
from unittest.mock import Mock

from objective.domain.objective import Objective
from objective.service.objectiveService import ObjectiveService


class TestObjectiveService(TestCase):
    def setUp(self) -> None:
        self.observer = Mock()
        self.service = ObjectiveService()
        self.test_objective = Objective("test_objective")

    def test_given_an_observer_when_service_updated_then_observer_is_updated(self) -> None:
        self.service.attach(self.observer)

        self.service.update_objective(self.test_objective)

        self.observer.update.assert_called_once()

    def test_given_updated_service_when_getting_objective_then_objectiveDTO_has_correct_value(self) -> None:
        self.service.update_objective(self.test_objective)

        objective_dto = self.service.get_objective()

        self.assertEqual(self.test_objective.value, objective_dto.value)
