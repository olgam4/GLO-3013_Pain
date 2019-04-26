import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from remote.domain.commandCallback import CommandCallback
from remote.domain.commandStatus import CommandStatus
from ui.domain.subroutine.iSubroutineRunner import ISubroutineRunner


class _DirectionalInput(ttk.Frame):
    def __init__(self, master, command: Callable[[], None], **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._command = command
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._button = ttk.Button(self, text="Go!", command=self._button_click, width=2)
        self._direction = tk.StringVar(value="")
        self._left = tk.Radiobutton(
            self, text="\u2190", value="left", variable=self._direction, indicatoron=False, borderwidth=2)
        self._up = tk.Radiobutton(
            self, text="\u2191", value="up", variable=self._direction, indicatoron=False, borderwidth=2)
        self._right = tk.Radiobutton(
            self, text="\u2192", value="right", variable=self._direction, indicatoron=False, borderwidth=2)
        self._down = tk.Radiobutton(
            self, text="\u2193", value="down", variable=self._direction, indicatoron=False, borderwidth=2)
        self._up_left = tk.Radiobutton(
            self, text="\u2196", value="upLeft", variable=self._direction, indicatoron=False, borderwidth=2)
        self._up_right = tk.Radiobutton(
            self, text="\u2197", value="upRight", variable=self._direction, indicatoron=False, borderwidth=2)
        self._down_right = tk.Radiobutton(
            self, text="\u2198", value="downRight", variable=self._direction, indicatoron=False, borderwidth=2)
        self._down_left = tk.Radiobutton(
            self, text="\u2199", value="downLeft", variable=self._direction, indicatoron=False, borderwidth=2)

    def draw(self, **kwargs) -> None:
        self.grid(**kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self._button.grid(row=1, column=1)
        self._left.grid(row=1, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        self._up.grid(row=0, column=1)
        self._right.grid(row=1, column=2)
        self._down.grid(row=2, column=1)
        self._up_left.grid(row=0, column=0)
        self._up_right.grid(row=0, column=2)
        self._down_right.grid(row=2, column=2)
        self._down_left.grid(row=2, column=0)
        self.config(borderwidth=2, relief='groove', padding='2p')

    def get(self) -> str:
        return self._direction.get()

    def _button_click(self) -> None:
        self._command()


class _SpeedInput(ttk.Frame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._speed = tk.StringVar(value="")
        self._fast = tk.Radiobutton(
            self, text="fast", value="fast", variable=self._speed, indicatoron=False, borderwidth=2)
        self._slow = tk.Radiobutton(
            self, text="slow", value="slow", variable=self._speed, indicatoron=False, borderwidth=2)

    def draw(self, **kwargs) -> None:
        self.grid(**kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._fast.grid(row=0, column=0, sticky=tk.W + tk.E)
        self._slow.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.config(borderwidth=2, relief='groove', padding='2p')

    def get(self) -> str:
        return self._speed.get()


class DirectionalControl(ttk.Frame):
    def __init__(self, master, subroutine_runner: ISubroutineRunner, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._subroutine_runner = subroutine_runner
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._title = ttk.Label(self, text="directional input")
        self._distance_label = ttk.Label(self, text="Distance (cm)")
        self._distance = tk.Spinbox(self, from_=0, to=150, increment=5)
        self._speed_input = _SpeedInput(self)
        self._directional_input = _DirectionalInput(self, self._directional_button_click)
        self._angle_label = ttk.Label(self, text="Angle (-0.5 < x < 0.5)")
        self._angle = tk.Spinbox(self, from_=-0.5, to=0.5, increment=0.05)
        self._rotational_button = ttk.Button(self, text="Turn!", command=self._rotational_button_click)
        self._progress = ttk.Progressbar(self, mode='indeterminate')

    def draw(self, **kwargs) -> None:
        self.config(borderwidth=2, relief='groove', padding='2p')
        self.grid(**kwargs)
        self._title.grid(columnspan=3, sticky=tk.N)
        self._distance_label.grid(row=1, column=0, sticky=tk.W + tk.S)
        self._distance.grid(row=2, column=0, sticky=tk.N)
        self._speed_input.draw(row=1, column=1, rowspan=2)
        self._directional_input.draw(row=1, column=2, rowspan=2)
        self._angle_label.grid(row=3, column=0, sticky=tk.W + tk.S)
        self._angle.grid(row=4, column=0, sticky=tk.N)
        self._rotational_button.grid(row=3, column=1, rowspan=2, columnspan=2)
        self._progress.grid(columnspan=3, sticky=tk.W + tk.E + tk.S)

    def _directional_button_click(self) -> None:
        direction = self._directional_input.get()
        speed = self._speed_input.get()
        if direction == "" or speed == "":
            messagebox.showwarning(title="No selection", message="Please make a selection")
            return

        try:
            self._subroutine_runner.execute_directional_movement(direction, speed, self._distance.get(),
                                                                 CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _rotational_button_click(self) -> None:
        try:
            self._subroutine_runner.execute_rotational_movement(self._angle.get(),
                                                                CommandCallback(self._button_click_done))
            self._progress.start()
        except BlockingIOError:
            messagebox.showerror(title="Impossible to comply", message="Already taking over the world.")

    def _button_click_done(self, status: CommandStatus) -> None:
        self._progress.stop()
