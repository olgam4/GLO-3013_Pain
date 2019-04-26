from typing import List

from cortex.domain.cortexError import NoItemMatched
from cortex.domain.iItemChooser import IItemChooser
from cortex.domain.objective.item import Item
from cortex.domain.objective.objective import Objective


class ItemChooser(IItemChooser):
    def choose_from(self, objective: Objective, items: List[Item]) -> List[Item]:
        items_string = ""
        chosen_items = []
        for item in items:
            items_string += str(item)
            if item.shape == objective.shape or item.color == objective.color:
                chosen_items.append(item)
        print(items_string)
        if len(chosen_items) == 0:
            raise NoItemMatched
        return chosen_items
