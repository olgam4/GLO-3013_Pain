import tkinter as tk
from tkinter import ttk, messagebox

from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner
from ui.domain.subroutine.subroutine import Subroutine


class MagnetSubroutine(Subroutine):
    def __init__(self, master, subroutine_runner: ISubroutineRunner):
        super().__init__(master, subroutine_runner)
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="Magnet")
        self._grab_button = ttk.Button(self, text="Grab", command=self._grab_click)
        self._drop_button = ttk.Button(self, text="Drop", command=self._drop_click)
        self._discharge_button = ttk.Button(self, text="Discharge", command=self._discharge_click)
        self._progress = ttk.Progressbar(self, mode='indeterminate')

    def draw(self) -> None:
        self.config(borderwidth=2, relief='groove', padding='2p')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self._title.grid(sticky=tk.N, columnspan=2)
        self._grab_button.grid(row=1, column=0)
        self._drop_button.grid(row=1, column=1)
        self._discharge_button.grid(columnspan=2)
        self._progress.grid(sticky=tk.W + tk.E + tk.S, columnspan=2)

    def _grab_click(self) -> None:
        try:
            self._subroutine_runner.execute_activate_magnet(CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _drop_click(self) -> None:
        try:
            self._subroutine_runner.execute_deactivate_magnet(CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _discharge_click(self) -> None:
        try:
            self._subroutine_runner.execute_discharge_magnet(CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _button_click_done(self, status: CommandStatus) -> None:
        self._progress.stop()
