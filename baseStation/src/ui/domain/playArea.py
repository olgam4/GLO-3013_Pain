import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

from application.domain.iObserver import IObserver
from pathDrawing.service.pathDrawingService import PathDrawingService
from vision.service.visionService import VisionService


class PlayArea(ttk.Frame, IObserver):
    def __init__(self, master, path_drawer_service: PathDrawingService, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._path_drawer_service = path_drawer_service
        self._path_drawer_service.attach(self)
        self._create_widgets()
        self._image_id = 0
        self._image: PhotoImage = None

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="World Camera")
        self._canvas = tk.Canvas(self, height=200, width=400, background='#B4B4B4')

    def draw(self, **kwargs) -> None:
        self.grid(**kwargs)
        self._title.grid()
        self._canvas.grid()

    def update(self) -> None:
        width, height = self._canvas.winfo_width(), self._canvas.winfo_height()
        vision_image = self._path_drawer_service.current_path_image.resize(width, height).as_rgb()
        self._image = ImageTk.PhotoImage(image=Image.fromarray(vision_image))
        self._canvas.delete(self._image_id)
        self._image_id = self._canvas.create_image(width / 2, height / 2, image=self._image)
