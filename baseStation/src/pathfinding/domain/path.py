from json import loads
from typing import List

from pathfinding.domain.movement import Movement


class Path:
    def __init__(self, movements: List[Movement]):
        self._movements = movements

    @property
    def movements(self) -> List[Movement]:
        return self._movements

    @classmethod
    def deserialize(cls, data: str):
        deserialized = loads(data)
        return Path([Movement.deserialize(movement_data) for movement_data in deserialized["movements"]])
