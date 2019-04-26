from logging import getLogger
from os import path
from threading import Event, Lock
from time import sleep
from typing import List

from application.domain.iObserver import IObserver
from pathfinding.domain.coord import Coord
from pathfinding.domain.position import Position
from vision.domain.iCamera import ICamera
from vision.domain.iCameraCalibration import ICameraCalibration
from vision.domain.iCameraCalibrationFactory import ICameraCalibrationFactory
from vision.domain.iCameraFactory import ICameraFactory
from vision.domain.iGoalFinder import IGoalFinder
from vision.domain.iImageDrawer import IImageDrawer
from vision.domain.iObstacleFinder import IObstacleFinder
from vision.domain.iPlayAreaFinder import IPlayAreaFinder
from vision.domain.iRobotFinder import IRobotFinder
from vision.domain.iSourceFinder import ISourceFinder
from vision.domain.image import Image
from vision.domain.rectangle import Rectangle
from vision.domain.visionError import VisionError, VisionFactoryError
from vision.service.visionServiceError import VisionServiceNotInitialized

logger = getLogger(__name__)


class VisionService:
    def __init__(self, camera_factory: ICameraFactory, camera_calibration_factory: ICameraCalibrationFactory,
                 image_drawer: IImageDrawer, play_area_finder: IPlayAreaFinder, goal_finder: IGoalFinder,
                 source_finder: ISourceFinder, obstacle_finder: IObstacleFinder, robot_finder: IRobotFinder) -> None:
        self._camera_factory = camera_factory
        self._camera_calibration_factory = camera_calibration_factory
        self._image_drawer = image_drawer
        self._play_area_finder = play_area_finder
        self._goal_finder = goal_finder
        self._source_finder = source_finder
        self._obstacles_finder = obstacle_finder
        self._robot_finder = robot_finder
        self._observers: List[IObserver] = []
        self._camera: ICamera = None
        self._camera_calibration: ICameraCalibration = None
        self._image: Image = None
        self._home: Rectangle = None
        self._goal: Rectangle = None
        self._source: Rectangle = None
        self._robot: Coord = None
        self._obstacles: List[Rectangle] = []
        self._initialized = Event()
        self._lock = Lock()

    def get_camera_ids(self) -> List[str]:
        cameras = self._camera_factory.get_cameras()
        return ['{}'.format(i) for i in cameras]

    def set_camera(self, camera_id: str, camera_calibration_file_path: path) -> None:
        self._camera = self._camera_factory.create_camera(int(camera_id))

        calibration_created = False
        while not calibration_created:
            self._image = self._camera.take_picture()
            try:
                self._camera_calibration = self._camera_calibration_factory.load_calibration_from_file(
                    camera_calibration_file_path, self._image)
                calibration_created = True
            except VisionFactoryError as e:
                logger.info(e.message)
                sleep(1)

        self._image = self._camera_calibration.rectify_image(self._image)
        self._initialized.set()

    def update(self) -> None:
        if not self._initialized.is_set():
            return

        # with self._lock:
        self._image = self._camera.take_picture()
        self._image = self._camera_calibration.rectify_image(self._image)
        self._notify()

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update()

    def get_image(self) -> Image:
        if not self._initialized.is_set():
            raise VisionServiceNotInitialized

        display_image = self._image.copy()
        display_image = self._image_drawer.draw_goal(display_image, self._goal)
        display_image = self._image_drawer.draw_obstacles(display_image, self._obstacles)
        display_image = self._image_drawer.draw_source(display_image, self._source)
        play_area = self._play_area_finder.find(self._image)

        return display_image.crop(play_area)

    def get_goal(self) -> Position:
        if not self._initialized.is_set():
            raise VisionServiceNotInitialized

        self._goal, goal_orientation = self._goal_finder.find(self._image)

        goal_coord = self._camera_calibration.convert_table_pixel_to_real(self._goal.get_center())
        logger.info('[get_goal] x: {}, y: {}, orientation: {}'.format(goal_coord.x, goal_coord.y, goal_orientation))
        return Position(goal_coord, goal_orientation)

    def get_source(self) -> Position:
        if not self._initialized.is_set():
            raise VisionServiceNotInitialized

        self._source, source_orientation = self._source_finder.find(self._image)

        source_coord = self._camera_calibration.convert_table_pixel_to_real(self._source.get_center())
        logger.info(
            '[get_source] x: {}, y: {}, orientation: {}'.format(source_coord.x, source_coord.y, source_orientation))
        return Position(source_coord, source_orientation)

    def get_obstacles(self) -> List[Coord]:
        if not self._initialized.is_set():
            raise VisionServiceNotInitialized

        self._obstacles = self._obstacles_finder.find(self._image)
        obstacles_coord = []
        for i in range(len(self._obstacles)):
            obstacles_coord.append(self._camera_calibration.convert_obstacle_pixel_to_real(self._obstacles[i].get_center()))
            logger.info('[get_obstacles] x: {}, y: {}'.format(obstacles_coord[i].x, obstacles_coord[i].y))
        return obstacles_coord

    def get_robot(self) -> Position:
        if not self._initialized.is_set():
            raise VisionServiceNotInitialized

        self._robot, robot_orientation = self._robot_finder.find(self._image)

        robot_coord = self._camera_calibration.convert_robot_pixel_to_real(self._robot)
        logger.debug(
            '[get_robot] x: {}, y: {}, orientation: {}'.format(robot_coord.x, robot_coord.y, robot_orientation))
        return Position(robot_coord, robot_orientation)
