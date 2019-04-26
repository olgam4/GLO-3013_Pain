import tkinter as tk
from tkinter import ttk, messagebox

from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from timer.service.timeService import TimeService
from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner
from ui.domain.subroutine.subroutine import Subroutine


class ChampionshipSubroutine(Subroutine):
    def __init__(self, master, subroutine_runner: ISubroutineRunner, time_service: TimeService) -> None:
        super().__init__(master, subroutine_runner)
        self._time_service = time_service
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="Championship routine")
        self._button = ttk.Button(self, text="Go!", command=self._button_click)
        self._progress = ttk.Progressbar(self, mode='indeterminate')

    def draw(self) -> None:
        self.config(borderwidth=2, relief='groove', padding='2p')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self._title.grid(sticky=tk.N)
        self._button.grid()
        self._progress.grid(sticky=tk.W + tk.E + tk.S)

    def _button_click(self) -> None:
        try:
            self._subroutine_runner.execute_championship_subroutine(CommandCallback(self._button_click_done))
            self._progress.start()
            self._time_service.reset()
            self._time_service.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _button_click_done(self, status: CommandStatus) -> None:
        self._progress.stop()
        self._time_service.stop()
