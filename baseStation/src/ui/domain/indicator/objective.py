import tkinter as tk
from tkinter import ttk

from objective.service.objectiveService import ObjectiveService
from application.domain.iObserver import IObserver


class Objective(ttk.Frame, IObserver):
    def __init__(self, master, objective_service: ObjectiveService, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._objective_service = objective_service
        self._objective_service.attach(self)
        self._create_widgets()

    def _create_widgets(self) -> None:
        # self._image_var = tk.PhotoImage()
        # self._image = tk.Canvas(self, height='120p', width='120p')
        self._text_var = tk.StringVar(value="code not read yet")
        self._text = ttk.Label(self, textvariable=self._text_var)

    def draw(self, **kwargs) -> None:
        self.config(borderwidth=2, relief='groove', padding='2p')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.grid(**kwargs)
        # self._image.grid()
        self._text.config(borderwidth=2, relief='groove')
        self._text.grid()

    def update(self) -> None:
        objective_dto = self._objective_service.get_objective()
        self._text_var.set(objective_dto.value)
