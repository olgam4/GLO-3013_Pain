import tkinter as tk
from tkinter import ttk

from light.service.lightService import LightService
from application.domain.iObserver import IObserver


class Light(ttk.Frame, IObserver):
    def __init__(self, master, light_service: LightService, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._light_service = light_service
        self._light_service.attach(self)
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._label_off = ttk.Label(self, text="Off")
        self._label_on = ttk.Label(self, text="On")
        self._slider = ttk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL)
        self._slider.state(['disabled'])

    def draw(self, **kwargs) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(**kwargs)
        self._label_off.grid(row=0, column=0, sticky=tk.E)
        self._slider.grid(row=0, column=1)
        self._label_on.grid(row=0, column=2, sticky=tk.W)

    def update(self) -> None:
        light_dto = self._light_service.get_light()
        self._slider.state(['!disabled'])
        if light_dto.is_on:
            self._slider.set(1)
        else:
            self._slider.set(0)
        self._slider.state(['disabled'])
