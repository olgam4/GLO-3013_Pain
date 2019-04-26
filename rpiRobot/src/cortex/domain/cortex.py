from logging import getLogger

from cortex.domain.dexterityCortex import DexterityCortex
from cortex.domain.directionCortex import DirectionCortex
from cortex.domain.iCommunicationCortex import ICommunicationCortex
from cortex.domain.iNapCortex import INapCortex
from cortex.domain.iVisualCortex import IVisualCortex
from cortex.domain.objective.objective import Objective
from vision.domain.visionError import VisionError

logger = getLogger(__name__)


class Cortex:
    def __init__(self, communication_cortex: ICommunicationCortex, visual_cortex: IVisualCortex,
                 direction_cortex: DirectionCortex, nap_cortex: INapCortex, dexterity_cortex: DexterityCortex) -> None:
        self._communication_cortex = communication_cortex
        self._visual_cortex = visual_cortex
        self._direction_cortex = direction_cortex
        self._nap_cortex = nap_cortex
        self._dexterity_cortex = dexterity_cortex
        self._objective = None

    def run(self) -> None:
        self._direction_cortex.update_directions()

        self.charge_subroutine()
        self.read_qr_subroutine()
        self.grab_subroutine(self._objective)
        self.drop_subroutine(self._objective)

        self.go_home_subroutine()
        self._communication_cortex.announce_win()

    def charge_subroutine(self) -> None:
        self._nap_cortex.recharge()

    def go_home_subroutine(self) -> None:
        self._direction_cortex.reach_home()

    def read_qr_subroutine(self) -> None:
        found_objective = False
        while not found_objective:
            self._direction_cortex.reach_qr_code()
            try:
                self._objective = self._visual_cortex.find_objective()
                found_objective = True
            except VisionError as e:  # TODO cortex domain error
                logger.debug(e.message)

    def grab_subroutine(self, objective: Objective) -> None:
        self._dexterity_cortex.grab(objective)

    def drop_subroutine(self, objective: Objective) -> None:
        self._dexterity_cortex.drop(objective)
