from unittest import TestCase

from cortex.domain.objective.color import Color
from cortex.domain.objective.shape import Shape
from vision.service.objectiveParser import ObjectiveParser


class TestObjectiveParser(TestCase):
    def setUp(self) -> None:
        self.objective_parser = ObjectiveParser()

    def test_given_an_objective_string_with_a_shape_when_parsing_then_it_returns_the_correct_objective(self) -> None:
        objective = self.objective_parser.parse('14-pentagone-Zone3')

        self.assertEqual(Shape.Pentagon, objective.shape)
        self.assertEqual(Color.NoColor, objective.color)
        self.assertEqual(3, objective.destination)

    def test_given_an_objective_string_with_a_color_when_parsing_then_it_returns_the_correct_objective(self) -> None:
        objective = self.objective_parser.parse('2-bleu-Zone1')

        self.assertEqual(Shape.NoShape, objective.shape)
        self.assertEqual(Color.Blue, objective.color)
        self.assertEqual(1, objective.destination)

    def test_given_an_objective_string_with_a_destination_when_parsing_then_it_returns_the_correct_objective(self) -> None:
        objective = self.objective_parser.parse('2-bleu-Zone11')

        self.assertEqual(11, objective.destination)
