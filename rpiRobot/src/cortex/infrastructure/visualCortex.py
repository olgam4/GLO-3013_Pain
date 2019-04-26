from logging import getLogger
from typing import List

from coordinate.cameraCoordinate import CameraCoordinate
from cortex.domain.iVisualCortex import IVisualCortex
from cortex.domain.objective.item import Item
from cortex.domain.objective.objective import Objective
from cortex.infrastructure.itemAssembler import ItemAssembler
from sight.service.sightService import SightService
from vision.domain.visionError import VisionError
from vision.infrastructure.openCvVisionError import CouldNotFindItemsError, CouldNotFindDestinationError
from vision.service.visionService import VisionService

logger = getLogger(__name__)


class VisualCortex(IVisualCortex):
    find_items_frames_count = 10

    def __init__(self, vision_service: VisionService, sight_service: SightService):
        self._vision_service = vision_service
        self._sight_service = sight_service

    def find_objective(self) -> Objective:
        """
        includes visualising qrCode, realigning if needed, and decoding it
        """
        self._sight_service.look_ahead()
        try:
            self._vision_service.update()
            return self._vision_service.read_objective()
        except VisionError as e:
            logger.error("could not read qr code")
            raise e

    def find_items(self) -> List[Item]:
        self._sight_service.look_down()
        items = []
        for i in range(self.find_items_frames_count):
            self._vision_service.update()
            try:
                items.extend(self._vision_service.find_items().items)
            except CouldNotFindItemsError:
                continue
        self._sight_service.look_ahead()
        return [ItemAssembler.from_item_relative_position(item) for item in items]

    def find_drop_position(self, objective: Objective) -> CameraCoordinate:
        self._sight_service.look_down()
        self._vision_service.update()
        try:
            destination_position = self._vision_service.find_destination_position(objective.destination)
        except CouldNotFindDestinationError as e:
            self._vision_service.save_image()
            raise e
        finally:
            self._sight_service.look_ahead()
        return CameraCoordinate(destination_position.x / 10, destination_position.y / 10)
