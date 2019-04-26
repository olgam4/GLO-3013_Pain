from os import path

import cv2
import numpy as np

from vision.domain.iCameraCalibration import ICameraCalibration
from vision.domain.iCameraCalibrationFactory import ICameraCalibrationFactory
from vision.domain.iPlayAreaFinder import IPlayAreaFinder
from vision.domain.image import Image
from vision.infrastructure.cvCamera import CvCamera
from vision.infrastructure.cvCameraCalibration import CvCameraCalibration
from vision.infrastructure.cvPlayAreaFinder import CvPlayAreaFinder
from vision.infrastructure.cvVisionException import CameraCalibrationCouldNotBeCreatedUsingImage, \
    PlayAreaCouldNotBeFound


class CvCameraCalibrationFactory(ICameraCalibrationFactory):
    def __init__(self, play_area_finder: IPlayAreaFinder):
        self._play_area_finder = play_area_finder

    def load_calibration_from_file(self, calibration_file_path: path, image: Image) -> ICameraCalibration:
        arrays = np.load(calibration_file_path)
        camera_matrix = arrays['camera_matrix']
        distortion_coefficients = arrays['distortion_coefficients']

        try:
            return CvCameraCalibration(camera_matrix, distortion_coefficients, self._play_area_finder, image)
        except PlayAreaCouldNotBeFound:
            raise CameraCalibrationCouldNotBeCreatedUsingImage


def main() -> None:
    calibration_file_path = "/home/loup/Projects/glo-3013/doc/calib_table_6.npz"
    camera = CvCamera(2)
    factory = CvCameraCalibrationFactory(CvPlayAreaFinder())
    calibration = factory.load_calibration_from_file(calibration_file_path, camera.take_picture())
    while True:
        rectified_image = calibration.rectify_image(camera.take_picture())
        cv2.imshow("rectified image", rectified_image.content)
        cv2.waitKey(0)


if __name__ == "__main__":
    main()
