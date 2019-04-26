from time import time

from cv2.cv2 import imwrite

from coordinate.cameraCoordinate import CameraCoordinate
from cortex.domain.objective.objective import Objective
from vision.domain.iCameraCalibrationFactory import ICameraCalibrationFactory
from vision.domain.iCameraFactory import ICameraFactory
from vision.domain.iDestinationFinder import IDestinationFinder
from vision.domain.iItemFinder import IItemFinder
from vision.domain.iQrCodeReader import IQrCodeReader
from vision.domain.itemRelativePosition import ItemRelativePosition
from vision.domain.itemRelativePositions import ItemRelativePositions
from vision.service.imageAssembler import ImageAssembler
from vision.service.objectiveParser import ObjectiveParser

camera_calibration_file_path = "doc/calib_robot.npz"


class VisionService:
    def __init__(self, camera_factory: ICameraFactory, camera_calibration_factory: ICameraCalibrationFactory,
                 qr_code_reader: IQrCodeReader, item_finder: IItemFinder, destination_finder: IDestinationFinder,
                 objective_parser: ObjectiveParser):
        self._camera_factory = camera_factory
        self._camera = self._camera_factory.create_camera()
        self._create_camera_calibration(camera_calibration_factory)
        self._qr_code_reader = qr_code_reader
        self._item_finder = item_finder
        self._destination_finder = destination_finder
        self._image = None
        self._objective_parser = objective_parser
        self._objective_text = ""

    def _create_camera_calibration(self, camera_calibration_factory: ICameraCalibrationFactory) -> None:
        image = self._camera.take_picture()
        self._camera_calibration = camera_calibration_factory.load_calibration_from_file(camera_calibration_file_path,
                                                                                         image.width, image.height)

    def update(self) -> None:
        image = self._camera.take_picture()
        self._image = self._camera_calibration.rectify_image(image)

    def get_image(self) -> str:
        return ImageAssembler.to_string(self._image)

    def save_image(self) -> None:
        imwrite("/home/pi/Pictures/debugGoal/{}.png".format(time()), self._image.content)

    def find_items(self) -> ItemRelativePositions:
        item_relative_positions_pixel = self._item_finder.find_items(self._image)
        item_relative_positions_real = []
        for item_relative_position_pixel in item_relative_positions_pixel.items:
            pixel_position = item_relative_position_pixel.camera_coordinate
            real_position = self._camera_calibration.convert_pixel_to_real(pixel_position)
            item_relative_position_real = ItemRelativePosition(item_relative_position_pixel.item, real_position)
            item_relative_positions_real.append(item_relative_position_real)
        return ItemRelativePositions(item_relative_positions_real)

    def find_destination_position(self, destination: int) -> CameraCoordinate:
        coordinate_pixel = self._destination_finder.find_destination(self._image, destination)
        return self._camera_calibration.convert_pixel_to_real(coordinate_pixel)

    def read_objective(self) -> Objective:
        """
        reads the qrCode and converts it to an objective

        if code is unreadable: throws error
            (could specify movement for a better angle)
        """
        self._objective_text = self._qr_code_reader.read_qr_code(self._image)
        return self._objective_parser.parse(self._objective_text)

    def get_objective(self) -> str:
        return self._objective_text
