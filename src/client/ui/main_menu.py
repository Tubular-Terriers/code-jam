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


class Main_menu(UI):
    def __init__(self):
        super().__init__("main_menu_scr")
        self.message = [
            r" _   _                        _             ",
            r"| | | |                      (_)            ",
            r"| |_| |__   ___   ____   ___  _ _ __   __ _ ",
            r"| __|  _ \ / _ \ |  _ \ / _ \| |  _ \ / _  |",
            r"| |_| | | |  __/ | |_) | (_) | | | | | (_| |",
            r" \__|_| |_|\___| |  __/ \___/|_|_| |_|\__, |",
            r"                 | |                   __/ |",
            r"                 |_|                  |___/ ",
        ]

    async def view(self, app):
        # Required
        super().view(app)
        height, width = self.window.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, 215, curses.COLOR_BLACK)
        self.window.attron(curses.color_pair(2))

        y = 0
        for text in self.message:
            self.window.addstr(
                height // 2 - len(self.message) + y,
                width // 2 - len(text) // 2,
                text,
                curses.color_pair(2),
            )
            y += 1

        self.window.attroff(curses.color_pair(2))
        self.window.attroff(curses.A_BOLD)
        self.refresh()
        game_button = Button(
            (height // 2) + 3,
            (width // 2) - 15,
            key=keyboard.Key.space,
            go_to=AppState.GAME,
        )
        self.window.addstr(
            (height // 2) + 4, (width // 2) - 12, "Press Space to join a Game"
        )
        exit_button = Button(
            (height // 2) + 6,
            (width // 2) - 15,
            key=keyboard.Key.esc,
            go_to=AppState.EXIT,
        )
        self.window.addstr((height // 2) + 7, (width // 2) - 12, "Press Escape to Exit")

        credit_button = Button(
            (height // 2) + 9,
            (width // 2) - 15,
            key="c",
            go_to=AppState.CREDITS_SCR,
        )
        self.window.addstr(
            (height // 2) + 10, (width // 2) - 12, "Press C to see credits"
        )
        self.input_manager = app.input_manager
        self.widgets = [game_button, exit_button, credit_button]
        self.register_input_managers(*self.widgets)
        self.refresh()
        res = None
        while True:
            if res := self.refresh():
                break
            curses.doupdate()
            await asyncio.sleep(0.1)
        return res


main_menu = Main_menu()
