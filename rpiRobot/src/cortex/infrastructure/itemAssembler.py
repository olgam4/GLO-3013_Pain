from coordinate.cameraCoordinate import CameraCoordinate
from cortex.domain.objective.color import Color as cortexColor
from cortex.domain.objective.item import Item
from cortex.domain.objective.shape import Shape as cortexShape
from vision.domain.item.color import Color as visionColor
from vision.domain.item.shape import Shape as visionShape
from vision.domain.itemRelativePosition import ItemRelativePosition


class ItemAssembler:
    @staticmethod
    def from_item_relative_position(item: ItemRelativePosition) -> Item:
        if item.item.color == visionColor.Red:
            color = cortexColor.Red
        elif item.item.color == visionColor.Green:
            color = cortexColor.Green
        elif item.item.color == visionColor.Blue:
            color = cortexColor.Blue
        else:
            color = cortexColor.Yellow
        if item.item.shape == visionShape.Triangle:
            shape = cortexShape.Triangle
        elif item.item.shape == visionShape.Square:
            shape = cortexShape.Square
        elif item.item.shape == visionShape.Pentagon:
            shape = cortexShape.Pentagon
        else:
            shape = cortexShape.Circle
        coordinate = CameraCoordinate(item.camera_coordinate.x / 10, item.camera_coordinate.y / 10)
        return Item(color, shape, coordinate)
