import cv2
import numpy as np

from vision.domain.iCameraCalibration import ICameraCalibration, camera_height_form_table_mm
from vision.domain.image import Image
from coordinate.cameraCoordinate import CameraCoordinate


class OpenCvCameraCalibration(ICameraCalibration):
    def __init__(self, camera_matrix: np.ndarray, distortion_coefficients: np.ndarray, image_width: int,
                 image_height: int) -> None:
        self._camera_matrix = camera_matrix
        self._distortion_coefficients = distortion_coefficients
        self._optimized_camera_matrix, self._region_of_interest = \
            cv2.getOptimalNewCameraMatrix(self._camera_matrix, self._distortion_coefficients,
                                          (image_width, image_height), 1, (image_width, image_height))
        self._camera_matrix_inverse = np.linalg.inv(self._optimized_camera_matrix)

    def rectify_image(self, image: Image) -> Image:
        return image.process(self._process_rectify)

    def _process_rectify(self, image: np.ndarray) -> np.ndarray:
        rectified_image = cv2.undistort(image, self._camera_matrix, self._distortion_coefficients, None,
                                        self._optimized_camera_matrix)

        region_of_interest_x, region_of_interest_y, roi_width, roi_height = self._region_of_interest
        return rectified_image[region_of_interest_y: region_of_interest_y + roi_height,
                               region_of_interest_x: region_of_interest_x + roi_width, :]

    def convert_pixel_to_real(self, coordinate_pixel: CameraCoordinate) -> CameraCoordinate:
        pixel_vector = np.array([coordinate_pixel.x, coordinate_pixel.y, 1]).transpose()

        real_vector = self._camera_matrix_inverse.dot(pixel_vector)
        real_vector = np.multiply(real_vector, camera_height_form_table_mm).transpose()

        return CameraCoordinate(real_vector[0], real_vector[1])
