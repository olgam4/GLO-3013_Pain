from tkinter import ttk
from typing import Callable

from ui.domain.directionalControl import DirectionalControl
from ui.domain.iMainView import IMainView
from ui.domain.indicator.indicators import Indicators
from ui.domain.onBoardCamera import OnBoardCamera
from ui.domain.subroutine.subroutines import Subroutines
from ui.domain.worldCameraSelector import WorldCameraSelector


class RemoteMainView(IMainView):
    def __init__(self, master, subroutines: Callable[[ttk.Frame], Subroutines],
                 world_camera_selector: Callable[[ttk.Frame], WorldCameraSelector],
                 on_board_camera: Callable[[ttk.Frame], OnBoardCamera],
                 directional_control: Callable[[ttk.Frame], DirectionalControl],
                 indicators: Callable[[ttk.Frame], Indicators]) -> None:
        super().__init__(master)
        self.master.title('Remote Control')
        self._world_camera_selector = world_camera_selector(self)
        self._on_board_camera = on_board_camera(self)
        self._directional_control = directional_control(self)
        self._subroutines = subroutines(self)
        self._indicators = indicators(self)

    def draw(self) -> None:
        self.grid()
        self._world_camera_selector.draw(row=0, column=0)
        self._on_board_camera.draw(row=0, column=1)
        self._directional_control.draw(row=1, column=0)
        self._subroutines.draw(row=1, column=1)
        self._indicators.draw(row=0, column=2, rowspan=2)
