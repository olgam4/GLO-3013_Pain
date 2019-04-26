from abc import ABC, abstractmethod

from vision.domain.image import Image


from coordinate.cameraCoordinate import CameraCoordinate

items_thickness_mm = 3
camera_height_form_table_mm = 242 - items_thickness_mm


class ICameraCalibration(ABC):
    @abstractmethod
    def rectify_image(self, image: Image) -> Image:
        pass

    @abstractmethod
    def convert_pixel_to_real(self, coordinate_pixel: CameraCoordinate) -> CameraCoordinate:
        pass
