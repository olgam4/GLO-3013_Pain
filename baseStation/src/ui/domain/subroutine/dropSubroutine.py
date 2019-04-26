import tkinter as tk
from tkinter import messagebox, ttk

from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from ui.domain.radioButtonGroup import RadioButtonGroup
from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner
from ui.domain.subroutine.subroutine import Subroutine


class DropSubroutine(Subroutine):
    def __init__(self, master, subroutine_runner: ISubroutineRunner) -> None:
        super().__init__(master, subroutine_runner)
        self._zone_target = tk.StringVar(value="")
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="Drop an object")
        self._zones = RadioButtonGroup(
            self, "Zones", ["0", "1", "2", "3"], self._zone_target)
        self._button = ttk.Button(self, text="Go!", command=self._button_click)
        self._progress = ttk.Progressbar(self, mode='indeterminate')

    def draw(self) -> None:
        self._title.grid(sticky=tk.N)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self._zones.draw()
        self._button.grid()
        self._progress.grid(sticky=tk.W + tk.E + tk.S)
        self.config(borderwidth=2, relief='groove', padding='2p')

    def _button_click(self) -> None:
        if self._zone_target.get() == "":
            messagebox.showwarning(title="No selection", message="Please make a selection")
            return
        try:
            self._subroutine_runner.execute_drop_subroutine(self._zone_target.get(),
                                                            CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _button_click_done(self, status: CommandStatus) -> None:
        self._progress.stop()
