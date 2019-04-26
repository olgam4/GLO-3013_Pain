from json import dumps
from typing import List

from cortex.domain.path.absoluteMovement import AbsoluteMovement


class AbsolutePath:
    def __init__(self, movements: List[AbsoluteMovement]):
        self._movements = movements

    @property
    def movements(self) -> List[AbsoluteMovement]:
        return self._movements

    def serialize(self) -> str:
        return dumps({
            "movements": [movement.serialize() for movement in self.movements]
        })

    def __eq__(self, other) -> bool:
        if not type(other) is AbsolutePath:
            return NotImplemented
        if len(self.movements) != len(other.movements):
            return False
        different = False
        for i in range(len(self.movements)):
            if self.movements[i] != other.movements[i]:
                different = True
                break
        return not different

    def __add__(self, other):
        if not type(other) is AbsolutePath:
            return NotImplemented
        movements = [movement for movement in self.movements]
        movements.extend(other.movements)
        return AbsolutePath(movements)

    def __repr__(self) -> str:
        representation = "{}[".format(AbsolutePath.__name__)
        movements_repr = ""
        for movement in self.movements:
            movements_repr += "{},".format(movement)
        return "{}{}]".format(representation, movements_repr[:-1])

