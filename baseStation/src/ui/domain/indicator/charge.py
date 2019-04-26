import tkinter as tk
from tkinter import ttk

from application.domain.iObserver import IObserver
from prehensor.service.prehensorService import PrehensorService


class Charge(ttk.Frame, IObserver):
    def __init__(self, master, prehensor_service: PrehensorService, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._prehensor_service = prehensor_service
        self._prehensor_service.attach(self)
        self._create_widgets()

    def _create_widgets(self) -> None:
        # self._label_zero = ttk.Label(self, text="empty")
        # self._label_full = ttk.Label(self, text="full")
        # self._slider = ttk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL)
        # self._slider.state(['disabled'])
        self._voltage_text_var = tk.StringVar(value="  0V")
        self._voltage = ttk.Label(self, textvariable=self._voltage_text_var)

    def draw(self, **kwargs) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(**kwargs)
        # self._label_zero.grid(row=0, column=0, sticky=tk.E)
        # self._slider.grid(row=0, column=1)
        # self._label_full.grid(row=0, column=2, sticky=tk.W)
        self._voltage.grid(row=0, column=3)

    def update(self) -> None:
        charge = self._prehensor_service.get_prehensor().charge
        # self._slider.state(['!disabled'])
        # self._slider.set(charge * 100)
        # self._slider.state(['disabled'])
        self._voltage_text_var.set(" {: 2.3f}V".format(charge * 35))
