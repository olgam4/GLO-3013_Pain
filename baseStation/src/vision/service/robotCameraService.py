from typing import List

from application.domain.iObserver import IObserver
from vision.domain.image import Image
from vision.service.imageAssembler import ImageAssembler


class RobotCameraService:
    def __init__(self) -> None:
        self._image: Image = None
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update()

    def update_image(self, image_text: str) -> None:
        self._image = ImageAssembler.to_image(image_text)
        self._notify()

    def get_image(self) -> Image:
        return Image(self._image.content)
