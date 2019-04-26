import tkinter as tk
from tkinter import ttk
from typing import List


class RadioButtonGroup(ttk.Frame):
    def __init__(self, master, title: str, elements: List[str], variable: tk.StringVar, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._elements: List[ttk.Radiobutton] = []
        self._create_widgets(title, elements, variable)

    def _create_widgets(self, title: str, elements: List[str], variable: tk.StringVar) -> None:
        self._title = ttk.Label(self, text=title)
        for element in elements:
            radio_button = ttk.Radiobutton(self, text=element, value=title + ':' + element, variable=variable)
            self._elements.append(radio_button)

    def draw(self, **kwargs) -> None:
        self.grid(**kwargs)
        self._title.grid()
        for button in self._elements:
            button.grid(sticky=tk.W)
