from math import pi
from unittest import TestCase

from mobility.domain.angle import Angle


class TestAngle(TestCase):
    def test_whenAngleIsBetweenMinusPiAndPi_thenEffectiveAngleIsBetweenMinusPiAndPi(self) -> None:
        angle = Angle(3 * pi / 4)

        effective_angle = Angle.to_effective(angle)

        self.assertEqual(angle, effective_angle)
        self.assertGreaterEqual(effective_angle, Angle(-pi))
        self.assertLessEqual(effective_angle, Angle(pi))

    def test_whenAngleIsLessThanMinusPi_thenEffectiveAngleIsBetweenMinusPiAndPi(self) -> None:
        angle = Angle(-5 * pi / 4)

        effective_angle = Angle.to_effective(angle)

        self.assertEqual(angle, effective_angle)
        self.assertGreaterEqual(effective_angle, Angle(-pi))
        self.assertLessEqual(effective_angle, Angle(pi))

    def test_whenAngleIsMoreThanPi_thenEffectiveAngleIsBetweenMinusPiAndPi(self) -> None:
        angle = Angle(5 * pi / 4)

        effective_angle = Angle.to_effective(angle)

        self.assertEqual(angle, effective_angle)
        self.assertGreaterEqual(effective_angle, Angle(-pi))
        self.assertLessEqual(effective_angle, Angle(pi))
