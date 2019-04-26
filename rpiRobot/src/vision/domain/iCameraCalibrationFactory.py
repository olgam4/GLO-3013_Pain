from abc import ABC, abstractmethod
from os import path

from vision.domain.iCameraCalibration import ICameraCalibration


class ICameraCalibrationFactory(ABC):
    @abstractmethod
    def load_calibration_from_file(self, calibration_file_path: path, image_width: int,
                                   image_height: int) -> ICameraCalibration:
        pass
