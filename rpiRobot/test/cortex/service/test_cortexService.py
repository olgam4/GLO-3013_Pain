from unittest import TestCase
from unittest.mock import Mock

from cortex.service.cortexService import CortexService


class TestCortexService(TestCase):
    def setUp(self) -> None:
        self.cortex = Mock()
        self.service = CortexService(self.cortex)

    def test_when_run_(self) -> None:
        self.service.run()

        self.assertTrue(self.cortex.run.called)
