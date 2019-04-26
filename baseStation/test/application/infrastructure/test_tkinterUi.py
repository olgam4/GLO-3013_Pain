from unittest import TestCase
from unittest.mock import Mock, call

from application.infrastructure.tkinterUi import TkinterUi


class TestTkinterUi(TestCase):
    def setUp(self) -> None:
        self.main_view = Mock()
        self.tkinter_ui = TkinterUi(self.main_view)

    def test_when_run_then_main_view_is_drawn(self) -> None:
        self.tkinter_ui.run()
        self.main_view.draw.assert_called()

    def test_when_run_then_main_view_mainloop_is_executed(self) -> None:
        self.tkinter_ui.run()
        self.main_view.mainloop.assert_called()

    def test_when_run_then_main_view_mainloop_is_executed_after_it_is_drawn(self) -> None:
        self.tkinter_ui.run()
        calls = self.main_view.mock_calls
        expected_calls = [call.draw(), call.mainloop()]
        self.assertListEqual(expected_calls, calls)
