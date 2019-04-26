from math import pi
from time import sleep
from typing import List

from coordinate.cameraCoordinate import CameraCoordinate
from cortex.domain.cortexError import NoItemMatched
from cortex.domain.directionCortex import DirectionCortex
from cortex.domain.iItemChooser import IItemChooser
from cortex.domain.iVisualCortex import IVisualCortex
from cortex.domain.objective.item import Item
from cortex.domain.objective.objective import Objective
from cortex.domain.path.cameraMovement import CameraMovement
from cortex.domain.path.cameraPath import CameraPath
from dexterity.service.dexterityService import DexterityService
from mobility.domain.angle import Angle
from mobility.domain.distance import Distance
from mobility.domain.operation.translateOperation import TranslateOperation
from mobility.service.mobilityService import MobilityService
from vision.infrastructure.openCvVisionError import CouldNotFindItemsError, CouldNotFindDestinationError


class DexterityCortex:
    prehensor_position = CameraCoordinate(2.5, 1.4)

    def __init__(self, mobility_service: MobilityService, dexterity_service: DexterityService,
                 direction_cortex: DirectionCortex, visual_cortex: IVisualCortex, item_chooser: IItemChooser) -> None:
        self._mobility_service = mobility_service
        self._dexterity_service = dexterity_service
        self._direction_cortex = direction_cortex
        self._visual_cortex = visual_cortex
        self._item_chooser = item_chooser

    def grab(self, objective: Objective) -> None:
        found_item = False
        items_in_source = []
        while not found_item:
            try:
                items_in_source = self._find_matching_items(objective)
            except NoItemMatched:
                continue
            except CouldNotFindItemsError:
                continue
            found_item = True
        items_left = [item for item in items_in_source]

        while len(items_left) == len(items_in_source):  # TODO check if specific item is left
            self._dexterity_service.let_go()
            chosen_item = items_in_source[0]
            path_to_item = self._path_to_position(chosen_item.position)
            self._mobility_service.drive(path_to_item)

            sleep(1)
            self._dexterity_service.grab()
            sleep(1)

            path_from_item = self._path_from_position(chosen_item.position)
            self._mobility_service.drive(path_from_item)

            try:
                items_left = self._find_matching_items(objective, False)
            except NoItemMatched:
                items_left = []
            except CouldNotFindItemsError:
                items_left = []

    def _find_matching_items(self, objective: Objective, move: bool = True) -> List[Item]:
        if move:
            self._mobility_service.operate([TranslateOperation(Angle(pi), Distance(5))])
            self._direction_cortex.reach_source()
            self._mobility_service.operate([TranslateOperation(Angle(pi / 2), Distance(1))])
        items = self._visual_cortex.find_items()
        return self._item_chooser.choose_from(objective, items)

    def drop(self, objective: Objective) -> None:
        found_destination = False
        position = None
        while not found_destination:
            try:
                position = self._find_destination(objective)
            except CouldNotFindDestinationError:
                print("CouldNotFindDestinationError")
                continue
            found_destination = True

        path_to_position = self._path_to_position(position)
        self._mobility_service.drive(path_to_position)

        self._dexterity_service.let_go()

        path_from_position = self._path_from_position(position)
        self._mobility_service.drive(path_from_position)

    def _find_destination(self, objective: Objective) -> CameraCoordinate:
        self._mobility_service.operate([TranslateOperation(Angle(pi), Distance(5))])
        self._direction_cortex.reach_goal()
        self._mobility_service.operate([TranslateOperation(Angle(pi / 2), Distance(1))])
        return self._visual_cortex.find_drop_position(objective)

    def _path_to_position(self, position: CameraCoordinate) -> CameraPath:
        movements = [CameraMovement(self.prehensor_position, position)]
        return CameraPath(movements)

    def _path_from_position(self, position: CameraCoordinate) -> CameraPath:
        movements = [CameraMovement(position, self.prehensor_position)]
        return CameraPath(movements)
