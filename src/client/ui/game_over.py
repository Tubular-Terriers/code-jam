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


class Game_over(UI):
    '''defines the game over screen'''
    def __init__(self):
        super().__init__("game_over_scr")
        self.message_text1 = "███▀▀▀██ ███▀▀▀███ ███▀█▄█▀███ ██▀▀▀"
        self.message_text2 = "██    ██ ██     ██ ██   █   ██ ██   "
        self.message_text3 = "██   ▄▄▄ ██▄▄▄▄▄██ ██   ▀   ██ ██▀▀▀"
        self.message_text4 = "██    ██ ██     ██ ██       ██ ██   "
        self.message_text5 = "███▄▄▄██ ██     ██ ██       ██ ██▄▄▄"
        self.message_text6 = "                                    "
        self.message_text7 = "███▀▀▀███ ▀███  ██▀ ██▀▀▀ ██▀▀▀▀██▄ "
        self.message_text8 = "██     ██   ██  ██  ██    ██     ██ "
        self.message_text9 = "██     ██   ██  ██  ██▀▀▀ ██▄▄▄▄▄▀▀ "
        self.message_text10 = "██     ██   ██  █▀  ██    ██     ██ "
        self.message_text11 = "███▄▄▄███    ▀█▀    ██▄▄▄ ██     ██▄"
        # print(self.message)

    async def view(self, app):
        # Required
        super().view(app)
        height, width = self.window.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        self.window.attron(curses.color_pair(2))
        self.window.attron(curses.A_BOLD)
        self.window.addstr(
            int((height / 2) - 7), int(width / 2) - 15, f"{self.message_text1}"
        )
        self.window.addstr(
            int((height / 2) - 6), int(width / 2) - 15, f"{self.message_text2}"
        )
        self.window.addstr(
            int((height / 2) - 5), int(width / 2) - 15, f"{self.message_text3}"
        )
        self.window.addstr(
            int((height / 2) - 4), int(width / 2) - 15, f"{self.message_text4}"
        )
        self.window.addstr(
            int((height / 2) - 3), int(width / 2) - 15, f"{self.message_text5}"
        )
        self.window.addstr(
            int((height / 2) - 2), int(width / 2) - 15, f"{self.message_text6}"
        )
        self.window.addstr(
            int((height / 2) - 1), int(width / 2) - 15, f"{self.message_text7}"
        )
        self.window.addstr(
            int((height / 2)), int(width / 2) - 15, f"{self.message_text8}"
        )
        self.window.addstr(
            int((height / 2) + 1), int(width / 2) - 15, f"{self.message_text9}"
        )
        self.window.addstr(
            int((height / 2) + 2), int(width / 2) - 15, f"{self.message_text10}"
        )
        self.window.addstr(
            int((height / 2) + 3), int(width / 2) - 15, f"{self.message_text11}"
        )
        self.window.attroff(curses.color_pair(2))
        self.window.attroff(curses.A_BOLD)
        self.refresh()
        menu_button = Button(
            (height // 2) + 5,
            (width // 2) - 15,
            key=keyboard.Key.space,
            go_to=AppState.MAIN_MENU,
        )
        self.window.addstr(
            (height // 2) + 6, (width // 2) - 12, "Press Space to go to Game menu"
        )
        exit_button = Button(
            (height // 2) + 8,
            (width // 2) - 15,
            key=keyboard.Key.esc,
            go_to=AppState.EXIT,
        )
        self.window.addstr((height // 2) + 9, (width // 2) - 12, "Press Escape to Exit")

        self.input_manager = app.input_manager
        self.widgets = [menu_button, exit_button]
        self.register_input_managers(*self.widgets)
        self.refresh()
        res = None
        while True:
            if res := self.refresh():
                break
            curses.doupdate()
            await asyncio.sleep(0.1)
        return res


game_over = Game_over()
