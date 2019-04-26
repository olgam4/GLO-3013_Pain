from abc import ABC, abstractmethod
from typing import List

from vision.domain.image import Image
from vision.domain.rectangle import Rectangle


class IImageDrawer(ABC):
    @abstractmethod
    def draw_goal(self, image: Image, goal: Rectangle) -> Image:
        pass

    @abstractmethod
    def draw_obstacles(self, image: Image, obstacles: List[Rectangle]) -> Image:
        pass

    @abstractmethod
    def draw_source(self, image: Image, source: Rectangle) -> Image:
        pass
