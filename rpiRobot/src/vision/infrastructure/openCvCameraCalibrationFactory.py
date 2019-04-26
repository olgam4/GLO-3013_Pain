from os import path

import numpy as np

from vision.domain.iCameraCalibration import ICameraCalibration
from vision.domain.iCameraCalibrationFactory import ICameraCalibrationFactory
from vision.infrastructure.fallbackCameraCalibration import FallBackCameraCalibration
from vision.infrastructure.openCvCameraCalibration import OpenCvCameraCalibration


class OpenCvCameraCalibrationFactory(ICameraCalibrationFactory):
    def load_calibration_from_file(self, calibration_file_path: path, image_width: int,
                                   image_height: int) -> ICameraCalibration:
        if calibration_file_path is None:
            return FallBackCameraCalibration()

        arrays = np.load(calibration_file_path)
        camera_matrix = arrays['camera_matrix']
        distortion_coefficients = arrays['distortion_coefficients']

        return OpenCvCameraCalibration(camera_matrix, distortion_coefficients, image_width, image_height)
