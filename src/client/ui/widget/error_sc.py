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
    def __init__(self):
        super().__init__("small_scr")
        self.message_text1 = "Sorry, your screen is too small."
        self.message_text2 = "please maximize your terminal and restart it."
        # print(self.message)

    async def view(self, app):
        # Required
        super().view(app)
        height, width = self.window.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        self.window.attron(curses.color_pair(2))
        self.window.addstr(
            int((height / 2) - 7), int(width / 2) - 15, f"{self.message_text1}"
        )
        self.window.addstr(
            int((height / 2) - 6), int(width / 2) - 15, f"{self.message_text2}"
        )
        self.window.attroff(curses.color_pair(2))
        self.refresh()


ss_error= Small_screen_error()
