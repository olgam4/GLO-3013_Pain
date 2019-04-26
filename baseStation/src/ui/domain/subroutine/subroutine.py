from tkinter import ttk

from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner


class Subroutine(ttk.Frame):
    def __init__(self, master, subroutine_runner: ISubroutineRunner) -> None:
        self._subroutine_runner: ISubroutineRunner = subroutine_runner
        super().__init__(master)

    def draw(self) -> None:
        pass
