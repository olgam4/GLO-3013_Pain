import tkinter as tk
from tkinter import messagebox, ttk

from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from ui.domain.radioButtonGroup import RadioButtonGroup
from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner
from ui.domain.subroutine.subroutine import Subroutine


class GrabSubroutine(Subroutine):
    def __init__(self, master, subroutine_runner: ISubroutineRunner) -> None:
        super().__init__(master, subroutine_runner)
        self._grab_target: tk.StringVar = tk.StringVar(value="")
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="Get an object")
        self._shapes = RadioButtonGroup(
            self, "Shapes", ["triangle", "square", "pentagon", "circle"], self._grab_target)
        self._colors = RadioButtonGroup(
            self, "Colors", ["blue", "green", "red", "yellow"], self._grab_target)
        self._button = ttk.Button(self, text="Go!", command=self._button_click)
        self._progress = ttk.Progressbar(self, mode='indeterminate')

    def draw(self) -> None:
        self._title.grid(columnspan=2, sticky=tk.N)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self._shapes.draw(row=1, column=0)
        self._colors.draw(row=1, column=1)
        self._button.grid(columnspan=2)
        self._progress.grid(columnspan=2, sticky=tk.W + tk.E + tk.S)
        self.config(borderwidth=2, relief='groove', padding='2p')

    def _button_click(self) -> None:
        if self._grab_target.get() == "":
            messagebox.showwarning(title="No selection", message="Please make a selection")
            return
        try:
            self._subroutine_runner.execute_grab_subroutine(self._grab_target.get(),
                                                            CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _button_click_done(self, status: CommandStatus) -> None:
        self._progress.stop()
