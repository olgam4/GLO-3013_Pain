from abc import ABC, abstractmethod

from pathfinding.domain.coord import Coord
from vision.domain.image import Image

table_width_mm: int = 2310
table_height_mm: int = 1110
obstacle_height_mm: int = 410
robot_height_mm: int = 220


class ICameraCalibration(ABC):
    @abstractmethod
    def rectify_image(self, image: Image) -> Image:
        pass

    @abstractmethod
    def convert_table_pixel_to_real(self, pixel: Coord) -> Coord:
        pass

    @abstractmethod
    def convert_obstacle_pixel_to_real(self, pixel: Coord) -> Coord:
        pass

    @abstractmethod
    def convert_robot_pixel_to_real(self, pixel: Coord) -> Coord:
        pass
