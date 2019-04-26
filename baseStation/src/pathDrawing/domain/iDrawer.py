from abc import ABC, abstractmethod

from pathfinding.domain.path import Path
from pathfinding.domain.position import Position
from vision.domain.image import Image


class IDrawer(ABC):
    @abstractmethod
    def draw(self, image: Image, path: Path):
        pass

    @abstractmethod
    def draw_robot(self, image: Image, position: Position):
        pass
