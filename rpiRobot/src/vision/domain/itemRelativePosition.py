from vision.domain.item.item import Item
from coordinate.cameraCoordinate import CameraCoordinate


class ItemRelativePosition:
    def __init__(self, item: Item, camera_coordinate: CameraCoordinate):
        self._item = item
        self._camera_coordinate = camera_coordinate

    @property
    def item(self) -> Item:
        return self._item

    @property
    def camera_coordinate(self) -> CameraCoordinate:
        return self._camera_coordinate
