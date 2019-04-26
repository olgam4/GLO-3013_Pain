from application.domain.iCerebrum import ICerebrum
from cortex.domain.cortex import Cortex


class CortexService(ICerebrum):
    def __init__(self, cortex: Cortex):
        self._cortex = cortex

    def run(self) -> None:
        self._cortex.run()
