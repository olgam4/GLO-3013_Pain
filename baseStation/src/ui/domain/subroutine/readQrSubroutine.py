import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from ui.domain.indicator.objective import Objective
from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner
from ui.domain.subroutine.subroutine import Subroutine


class ReadQrSubroutine(Subroutine):
    def __init__(self, master, subroutine_runner: ISubroutineRunner,
                 objective: Callable[[ttk.Frame], Objective]) -> None:
        super().__init__(master, subroutine_runner)
        self._objective = objective(self)
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="Move and read qr code")
        self._button = ttk.Button(self, text="Go!", command=self._button_click)
        self._progress = ttk.Progressbar(self, mode='indeterminate')

    def draw(self) -> None:
        self.config(borderwidth=2, relief='groove', padding='2p')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self._title.grid(sticky=tk.N)
        self._objective.draw()
        self._button.grid()
        self._progress.grid(sticky=tk.W + tk.E + tk.S)

    def _button_click(self) -> None:
        try:
            self._subroutine_runner.execute_read_qr_subroutine(CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _button_click_done(self, status: CommandStatus) -> None:
        self._progress.stop()
