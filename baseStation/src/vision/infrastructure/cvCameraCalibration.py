import cv2
import numpy as np

from pathfinding.domain.coord import Coord
from vision.domain.iCameraCalibration import ICameraCalibration, table_width_mm, table_height_mm, obstacle_height_mm, \
    robot_height_mm
from vision.domain.iPlayAreaFinder import IPlayAreaFinder
from vision.domain.image import Image
from vision.infrastructure.cvImageDisplay import CvImageDisplay


class CvCameraCalibration(ICameraCalibration):
    def __init__(self, camera_matrix: np.ndarray, distortion_coefficients: np.ndarray,
                 play_area_finder: IPlayAreaFinder, image: Image) -> None:
        self._play_area_finder = play_area_finder
        self._image_display = CvImageDisplay()
        self._camera_matrix = camera_matrix
        self._distortion_coefficients = distortion_coefficients
        self._optimized_camera_matrix, self._region_of_interest = \
            cv2.getOptimalNewCameraMatrix(self._camera_matrix, self._distortion_coefficients,
                                          image.size, 1, image.size)
        self._camera_matrix_inverse = np.linalg.inv(self._optimized_camera_matrix)

        self._focal_x: float = self._optimized_camera_matrix[0, 0]
        self._focal_y: float = self._optimized_camera_matrix[1, 1]
        self._compute_distances(image)

    def rectify_image(self, image: Image) -> Image:
        rectified_image = image.process(self._process_rectify)
        self._image_display.display_debug_image('[OpenCvCameraCalibration] rectified_image', rectified_image.content)
        return rectified_image

    def _process_rectify(self, image: np.ndarray) -> np.ndarray:
        rectified_image = cv2.undistort(image, self._camera_matrix, self._distortion_coefficients, None,
                                        self._optimized_camera_matrix)

        region_of_interest_x, region_of_interest_y, roi_width, roi_height = self._region_of_interest
        return rectified_image[region_of_interest_y: region_of_interest_y + roi_height,
                               region_of_interest_x: region_of_interest_x + roi_width, :]

    def _compute_distances(self, image: Image) -> None:
        table_roi = self._play_area_finder.find(image)

        table_distance_x = (table_width_mm * self._focal_x) / table_roi.width
        table_distance_y = (table_height_mm * self._focal_y) / table_roi.height

        self._table_distance = (table_distance_x + table_distance_y) / 2
        self._obstacle_distance = self._table_distance - obstacle_height_mm
        self._robot_distance = self._table_distance - robot_height_mm

        self._table_real_origin = self._convert_pixel_to_real(table_roi.top_left_corner, self._table_distance)

    def convert_table_pixel_to_real(self, pixel: Coord) -> Coord:
        return self._convert_object_pixel_to_real(pixel, self._table_distance)

    def convert_obstacle_pixel_to_real(self, pixel: Coord) -> Coord:
        return self._convert_object_pixel_to_real(pixel, self._obstacle_distance)

    def convert_robot_pixel_to_real(self, pixel: Coord) -> Coord:
        return self._convert_object_pixel_to_real(pixel, self._robot_distance)

    def _convert_pixel_to_real(self, pixel: Coord, distance: float) -> Coord:
        pixel_vector = np.array([pixel.x, pixel.y, 1]).transpose()

        real_vector = self._camera_matrix_inverse.dot(pixel_vector)
        real_vector = np.multiply(real_vector, distance).transpose()

        return Coord(int(real_vector[0]), int(real_vector[1]))

    def _adjust_real_to_table(self, real: Coord) -> Coord:
        return Coord(real.x - self._table_real_origin.x, real.y - self._table_real_origin.y)

    def _convert_object_pixel_to_real(self, pixel: Coord, distance: float) -> Coord:
        real = self._convert_pixel_to_real(pixel, distance)
        return self._adjust_real_to_table(real)
