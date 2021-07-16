import asyncio
import curses
import time
from time import sleep

from pynput import keyboard

from client.appstate import AppState

from ._ui import UI
from .widget.progress_bar import ProgressBar
from .widget.simple_button import Button
from .widget.simple_textbox import Box


class Small_screen_error(UI):
    """defines the ui error screen when the screen is way too small"""

    def __init__(self):
        super().__init__("small_scr")
        self.message_text1 = "Sorry, your screen is too small."
        self.message_text2 = "please maximize your terminal and restart it."
        # print(self.message)

    async def view(self, app):
        # Required
        super().view(app)
        self.height, self.width = self.window.getmaxyx()
        self.timeout = 10

        self.ch = int(self.height / 2)
        self.cw = int(self.width / 2)

        self.progress_bar = ProgressBar(
            height=1,
            width=30,
            y=self.ch - 5,
            x=self.cw - 15,
            message_text="Restarting in",
        )

        self.widgets = [self.progress_bar]

        for i in range(self.timeout):
            # This has nout
            # self.refresh()
            self.progress_bar.message = f"Restarting in {self.timeout} seconds..."
            self.progress_bar.set_progress(10 * i)
            self.draw()
            # calls widget to refresh
            self.refresh()
            curses.doupdate()
            await asyncio.sleep(1)
            self.timeout -= 1

        self.refresh()

    def draw(self):
        self.window.attron(curses.color_pair(2))
        self.window.addstr(
            self.ch - 7,
            self.cw - 15,
            f"{self.message_text1}",
        )
        self.window.addstr(
            self.ch - 6,
            self.cw - 15,
            f"{self.message_text2}",
        )
        self.window.attroff(curses.color_pair(2))


ss_error = Small_screen_error()
