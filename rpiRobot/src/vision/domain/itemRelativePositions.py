from typing import List

from vision.domain.itemRelativePosition import ItemRelativePosition


class ItemRelativePositions:
    def __init__(self, items: List[ItemRelativePosition]):
        self._items = items

    @property
    def items(self) -> List[ItemRelativePosition]:
        return self._items
