from math import pi, cos, sin

from pathDrawing.domain.iDrawer import IDrawer
from pathfinding.domain.coord import Coord
from pathfinding.domain.path import Path
from pathfinding.domain.position import Position
from vision.domain.image import Image
import cv2
from numpy import array

TABLE_WIDTH = 231
TABLE_HEIGHT = 111


class OpenCvDrawer(IDrawer):
    _old_points = []

    def draw(self, image: Image, path: Path) -> Image:
        image_content = image.content
        for movement in path.movements:
            start_relative_coords = self._get_coord_relative_to_table(image, movement.start)
            end_relative_coords = self._get_coord_relative_to_table(image, movement.end)
            start_coords = (start_relative_coords.x, start_relative_coords.y)
            end_coords = (end_relative_coords.x, end_relative_coords.y)
            cv2.line(image_content, start_coords, end_coords, (255, 0, 0), 5)
        return Image(image_content)

    def draw_robot(self, image: Image, position: Position) -> Image:
        image_content = image.content
        self._old_points.append(position)
        for i in range(len(self._old_points)):
            try:
                relative_position_start = self._get_coord_relative_to_table(image, self._old_points[i].coordinate)
                relative_position_end = self._get_coord_relative_to_table(image, self._old_points[i+1].coordinate)
            except IndexError:
                continue
            cv2.line(image_content, (relative_position_start.x, relative_position_start.y),
                     (relative_position_end.x, relative_position_end.y), (100, 100, 100), 1)
        start_relative_coords = self._get_coord_relative_to_table(image, position.coordinate)
        start_coords = (start_relative_coords.x, start_relative_coords.y)
        calculated_coords = self._calculate_coords_with_orientation(position)
        end_relative_coords = self._get_coord_relative_to_table(image, calculated_coords)
        end_coords = (end_relative_coords.x, end_relative_coords.y)
        cv2.line(image_content, start_coords, end_coords, (255, 0, 255), 4)
        return Image(image_content)

    def _get_coord_relative_to_table(self, image: Image, coord: Coord) -> Coord:
        width_image, height_image = image.size
        return Coord(int(coord.x * width_image / TABLE_WIDTH), int(coord.y * height_image / TABLE_HEIGHT))

    def _calculate_coords_with_orientation(self, position: Position):
        new_x = position.coordinate.x + 10 * sin(position.orientation.radians)
        new_y = position.coordinate.y - 10 * cos(position.orientation.radians)
        return Coord(new_x, new_y)
