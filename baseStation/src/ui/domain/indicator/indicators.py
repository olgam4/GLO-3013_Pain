import tkinter as tk
from tkinter import ttk
from typing import Callable

from ui.domain.indicator.charge import Charge
from ui.domain.indicator.light import Light
from ui.domain.indicator.objective import Objective
from ui.domain.indicator.timer import Timer


class Indicators(ttk.Frame):
    def __init__(self, master, objective: Callable[[ttk.Frame], Objective],
                 light: Callable[[ttk.Frame], Light], charge: Callable[[ttk.Frame], Charge],
                 timer: Callable[[ttk.Frame], Timer]) -> None:
        super().__init__(master)
        self._objective = objective(self)
        self._light = light(self)
        self._charge = charge(self)
        self._timer = timer(self)
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="System status")
        self._objective_label = ttk.Label(self, text="objective")
        self._light_label = ttk.Label(self, text="light status")
        self._charge_label = ttk.Label(self, text="charge")
        self._timer_label = ttk.Label(self, text="time")

    def draw(self, **kwargs) -> None:
        self.config(borderwidth=2, relief='groove', padding='2p')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.grid(**kwargs)
        self._title.grid(sticky=tk.N, columnspan=2)
        self._objective_label.grid(row=1, column=0)
        self._objective.draw(row=1, column=1)
        self._light_label.grid(row=2, column=0)
        self._light.draw(row=2, column=1)
        self._charge_label.grid(row=3, column=0)
        self._charge.draw(row=3, column=1)
        self._timer_label.grid(row=4, column=0)
        self._timer.draw(row=4, column=1)
