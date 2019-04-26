from tkinter import ttk
from typing import List

from ui.domain.subroutine.subroutine import Subroutine


class Subroutines(ttk.Notebook):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._subroutines: List[Subroutine] = []

    def add(self, child, **kw) -> None:
        self._subroutines.append(child)
        super().add(child, **kw)

    def draw(self, **kwargs) -> None:
        self.grid(**kwargs)
        for subroutine in self._subroutines:
            subroutine.draw()
