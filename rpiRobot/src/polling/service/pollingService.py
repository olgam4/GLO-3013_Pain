from typing import List

from cortex.domain.cortexError import NoItemMatched
from cortex.domain.iItemChooser import IItemChooser
from cortex.domain.objective.item import Item
from cortex.domain.objective.objective import Objective
from polling.domain.address import Address
from polling.domain.booth import Booth


class PollingService(IItemChooser):
    minimum_votes = 5

    def choose_from(self, objective: Objective, items: List[Item]) -> List[Item]:
        district = self._fill_district(items)
        chosen_items = []
        for booth in district:
            if booth.get_count() < self.minimum_votes:
                continue
            if booth.get_shape() == objective.shape or booth.get_color() == objective.color:
                chosen_items.append(Item(booth.get_color(), booth.get_shape(), booth.address.coordinate))
        if len(chosen_items) == 0:
            raise NoItemMatched
        print("\n{}\n".format(district))
        return chosen_items

    def _fill_district(self, items: List[Item]) -> List[Booth]:
        district = []
        for item in items:
            address = Address(item.position)
            address_booth = None
            found_booth = False
            for booth in district:
                if booth.address == address:
                    found_booth = True
                    address_booth = booth
                    break
            if not found_booth:
                address_booth = Booth(address)
                district.append(address_booth)
            address_booth.add_item(item)
        print("\n{}\n".format(district))
        return district
