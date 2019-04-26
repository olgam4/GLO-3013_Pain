from abc import ABC, abstractmethod
from os import path

from vision.domain.iCameraCalibration import ICameraCalibration
from vision.domain.image import Image


class ICameraCalibrationFactory(ABC):
    @abstractmethod
    def load_calibration_from_file(self, calibration_file_path: path, image: Image) -> ICameraCalibration:
        pass
