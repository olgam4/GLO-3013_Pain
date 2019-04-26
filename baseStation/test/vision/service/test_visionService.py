from unittest import TestCase
from unittest.mock import Mock

import numpy as np

from pathfinding.domain.angle import Angle
from pathfinding.domain.coord import Coord
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle
from vision.infrastructure.cvVisionException import CameraDoesNotExistError
from vision.service.visionService import VisionService


class TestVisionService(TestCase):
    valid_camera_ids_int = [0, 2]
    valid_camera_ids_str = ['0', '2']
    invalid_camera_id_int = 1
    invalid_camera_id_str = '1'
    calibration_file_path = 'path'
    image = Image(np.zeros((50, 50, 3)))

    def setUp(self) -> None:
        self.camera_factory = Mock()
        self.play_area_finder = Mock()
        self.goal_finder = Mock()
        self.source_finder = Mock()
        self.obstacle_finder = Mock()
        self.robot_finder = Mock()
        
        self.camera_calibration_factory = Mock()
        self.camera_calibration = Mock()
        self.camera_drawer = Mock()
        self.vision_service = VisionService(self.camera_factory, self.camera_calibration_factory, self.camera_drawer,
                                            self.play_area_finder, self.goal_finder, self.source_finder,
                                            self.obstacle_finder, self.robot_finder)

    def initialiseService(self) -> None:
        self.camera = Mock()
        self.camera_factory.create_camera = Mock(return_value=self.camera)
        self.camera.take_picture = Mock(return_value=self.image)
        self.camera_calibration_factory.load_calibration_from_file = Mock(return_value=self.camera_calibration)
        self.camera_calibration.rectify_image = Mock(return_value=self.image)

        self.vision_service.set_camera(self.valid_camera_ids_str[0], self.calibration_file_path)

    def test_when_service_first_created_then_it_is_not_initialized(self) -> None:
        self.assertFalse(self.vision_service._initialized.is_set())

    def test_when_camera_ids_requested_then_ids_from_camera_factory_returned_as_string(self) -> None:
        self.camera_factory.get_cameras = Mock(return_value=self.valid_camera_ids_int)
        expected_values = self.valid_camera_ids_str

        actual_values = self.vision_service.get_camera_ids()

        self.assertListEqual(expected_values, actual_values)

    def test_when_camera_set_with_valid_id_then_service_is_initialized(self) -> None:
        self.initialiseService()

        self.camera_factory.create_camera.assert_called_with(self.valid_camera_ids_int[0])
        self.camera.take_picture.assert_called_once()
        self.camera_calibration_factory.load_calibration_from_file.assert_called_with(self.calibration_file_path,
                                                                                      self.image)
        self.camera_calibration.rectify_image.assert_called_once()

        self.assertTrue(self.vision_service._initialized.is_set())

    def test_when_camera_set_with_invalid_id_then_CameraDoesNotExistError_is_raised(self) -> None:
        self.camera_factory.create_camera = Mock(side_effect=CameraDoesNotExistError(self.invalid_camera_id_int))

        self.assertRaises(CameraDoesNotExistError,
                          self.vision_service.set_camera, self.invalid_camera_id_str, self.calibration_file_path)

    def test_when_updated_then_attached_observers_are_notified(self) -> None:
        self.initialiseService()
        observer = Mock()
        self.vision_service.attach(observer)

        self.vision_service.update()

        observer.update.assert_called_once()

    def test_when_get_goal_then_center_of_goal_and_orientation_are_returned_as_real_coordinate(self) -> None:
        self.initialiseService()
        expected_coord = Coord(0, 0)
        expected_angle = Angle(0)
        self.goal_finder.find = Mock(return_value=(Rectangle(0, 0, 10, 8), expected_angle))
        self.camera_calibration.convert_table_pixel_to_real = Mock(return_value=Coord(0, 0))

        position = self.vision_service.get_goal()
        actual_coord = position.coordinate
        actual_angle = position.orientation

        self.camera_calibration.convert_table_pixel_to_real.assert_called_with(Coord(5, 4))
        self.assertEqual(expected_coord, actual_coord)
        self.assertEqual(expected_angle, actual_angle)

    def test_when_get_source_then_center_of_source_and_orientation_are_returned_as_real_coordinate(self) -> None:
        self.initialiseService()
        expected_coord = Coord(0, 0)
        expected_angle = Angle(0)
        self.source_finder.find = Mock(return_value=(Rectangle(0, 0, 10, 8), expected_angle))
        self.camera_calibration.convert_table_pixel_to_real = Mock(return_value=Coord(0, 0))

        position = self.vision_service.get_source()
        actual_coord = position.coordinate
        actual_angle = position.orientation

        self.camera_calibration.convert_table_pixel_to_real.assert_called_with(Coord(5, 4))
        self.assertEqual(expected_coord, actual_coord)
        self.assertEqual(expected_angle, actual_angle)
