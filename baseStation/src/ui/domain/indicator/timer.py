import tkinter as tk
from tkinter import ttk

from application.domain.iObserver import IObserver
from timer.service.timeService import TimeService


class Timer(ttk.Frame, IObserver):
    def __init__(self, master, time_service: TimeService, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._time_service = time_service
        self._time_service.attach(self)
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._time_var = tk.StringVar(value="")
        self._text = ttk.Label(self, textvariable=self._time_var)

    def draw(self, **kwargs) -> None:
        self.config(borderwidth=2, relief='groove', padding='2p')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(**kwargs)
        self._text.config(borderwidth=2, relief='groove')
        self._text.grid()

    def update(self) -> None:
        time = self._time_service.get_current_time()
        self._time_var.set(str(time))
