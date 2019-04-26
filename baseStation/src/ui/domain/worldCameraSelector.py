import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from pathDrawing.service.pathDrawingService import PathDrawingService
from ui.domain.playArea import PlayArea
from vision.service.visionService import VisionService


class WorldCameraSelector(ttk.Frame):
    def __init__(self, master, vision_service: VisionService, path_drawing_service: PathDrawingService,
                 **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._vision_service = vision_service
        self._path_drawing_service = path_drawing_service
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="World Camera Selector")
        self._create_camera_dropdown()
        self._play_area = PlayArea(self, self._path_drawing_service)

    def _create_camera_dropdown(self) -> None:
        camera_option = self._vision_service.get_camera_ids()
        self._camera_variable = tk.StringVar(self)
        self._camera_option_menu = ttk.Combobox(self, textvariable=self._camera_variable, values=camera_option)
        self._camera_variable.trace('w', self._change_camera_selection)

    def _change_camera_selection(self, *args) -> None:
        selected = self._camera_variable.get()

        camera_parameters_file_path = filedialog.askopenfilename(title='Select Camera Calibration File',
                                                                 filetypes=[('Numpy Files', '.npz')])

        if camera_parameters_file_path:
            self._vision_service.set_camera(selected, camera_parameters_file_path)

    def draw(self, **kwargs) -> None:
        self._clear_widgets()
        self.grid(**kwargs)
        self._title.grid()
        self._camera_option_menu.grid()
        self._play_area.draw()
        self.config(borderwidth=2, relief='groove', padding='2p')

    def _clear_widgets(self) -> None:
        for widget in self.children.values():
            widget.grid_forget()
