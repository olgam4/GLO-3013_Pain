from application.domain.iUi import IUi
from ui.domain.iMainView import IMainView


class TkinterUi(IUi):
    def __init__(self, main_view: IMainView):
        self._main_view: IMainView = main_view

    def run(self) -> None:
        self._main_view.draw()
        self._main_view.mainloop()
