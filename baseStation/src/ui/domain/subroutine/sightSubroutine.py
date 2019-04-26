import tkinter as tk
from tkinter import ttk, messagebox

from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner
from ui.domain.subroutine.subroutine import Subroutine


class SightSubroutine(Subroutine):
    def __init__(self, master, subroutine_runner: ISubroutineRunner)-> None:
        super().__init__(master, subroutine_runner)
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="Sight")
        self._look_ahead_button = ttk.Button(self, text="look ahead", command=self._look_ahead_click)
        self._look_down_button = ttk.Button(self, text="look down", command=self._look_down_click)
        self._progress = ttk.Progressbar(self, mode='indeterminate')

    def draw(self) -> None:
        self.config(borderwidth=2, relief='groove', padding='2p')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self._title.grid(sticky=tk.N, columnspan=2)
        self._look_ahead_button.grid(row=1, column=0)
        self._look_down_button.grid(row=1, column=1)
        self._progress.grid(sticky=tk.W + tk.E + tk.S, columnspan=2)

    def _look_ahead_click(self) -> None:
        try:
            self._subroutine_runner.execute_look_ahead(CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _look_down_click(self) -> None:
        try:
            self._subroutine_runner.execute_look_down(CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _button_click_done(self, status: CommandStatus) -> None:
        self._progress.stop()
