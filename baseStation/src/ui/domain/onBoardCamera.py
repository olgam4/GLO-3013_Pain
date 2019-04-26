import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

from application.domain.iObserver import IObserver
from vision.service.robotCameraService import RobotCameraService


class OnBoardCamera(ttk.Frame, IObserver):
    def __init__(self, master, robot_camera_service: RobotCameraService, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._robot_camera_service = robot_camera_service
        self._robot_camera_service.attach(self)
        self._create_widgets()
        self._image_id = 0
        self._image: PhotoImage = None

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="On Board Camera")
        self._canvas = tk.Canvas(self, height=200, width=400, background='#B4B4B4')

    def draw(self, **kwargs) -> None:
        self.grid(**kwargs)
        self._title.grid()
        self._canvas.grid()
        self.config(borderwidth=2, relief='groove', padding='2p')

    def update(self) -> None:
        width, height = self._canvas.winfo_width(), self._canvas.winfo_height()
        image = self._robot_camera_service.get_image().resize(width, height).as_rgb()
        self._image = ImageTk.PhotoImage(image=Image.fromarray(image))
        self._canvas.delete(self._image_id)
        self._image_id = self._canvas.create_image(width / 2, height / 2, image=self._image)
