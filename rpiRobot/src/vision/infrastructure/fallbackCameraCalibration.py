from vision.domain.iCameraCalibration import ICameraCalibration
from vision.domain.image import Image

from coordinate.cameraCoordinate import CameraCoordinate


class FallBackCameraCalibration(ICameraCalibration):
    def rectify_image(self, image: Image) -> Image:
        return image

    def convert_pixel_to_real(self, coordinate_pixel: CameraCoordinate) -> CameraCoordinate:
        return coordinate_pixel
