from application.domain.iObserver import IObserver
from pathDrawing.domain.iDrawer import IDrawer
from pathfinding.domain.path import Path
from pathfinding.domain.position import Position
from pathfinding.service.pathService import PathService
from pathfinding.service.positionService import PositionService
from vision.domain.image import Image
from vision.service.visionService import VisionService


class PathDrawingService(IObserver):
    def __init__(self, drawer: IDrawer, vision_service: VisionService, path_service: PathService):
        self._drawer = drawer
        self._vision_service = vision_service
        self._vision_service.attach(self)
        self._path_service = path_service
        self._observers = []
        self._current_path_image = None

    def _draw_on(self, image: Image, path: Path) -> Image:
        return self._drawer.draw(image, path)

    @property
    def current_path_image(self) -> Image:
        if self._current_path_image:
            return self._current_path_image
        else:
            return self._vision_service.get_image()

    def update(self) -> None:
        new_image = self._vision_service.get_image()
        new_path = self._path_service.get_path()
        image_with_path = self._draw_on(new_image, new_path)
        robot_position = self._vision_service.get_robot()
        robot_position_in_centimeters = Position(robot_position.coordinate.to_centimeters(), robot_position.orientation)
        self._current_path_image = self._draw_robot_on(image_with_path, robot_position_in_centimeters)
        self._notify()

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update()

    def _draw_robot_on(self, image: Image, robot_position: Position) -> Image:
        return self._drawer.draw_robot(image, robot_position)


