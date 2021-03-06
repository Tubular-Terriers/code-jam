import asyncio
import curses
import random
import re

from pynput import keyboard

from client.appstate import AppState
from client.tools.browser import BrowserManager
from client.tools.clipboard import ClipboardManager

from ._ui import UI
from .widget.button import Button


class Auth(UI):
    """makes main screen ui"""

    def __init__(self):
        super().__init__("main_menu_scr")
        self.message = [
            r"  _____________________________  ",
            r" /                             \ ",
            r"|    _______________________    |",
            r"|   /       The poing       \   |",
            r"|   |         _____         |   |",
            r"|   |        |==   |        |   |",
            r"|   |        |  o. |        |   |",
            r"|   |        |__O__|        |   |",
            r"|   |                       |   |",
            r"|   | Insert disk 1 to begin|   |",
            r"|   \_______________________/   |",
            r"|  /|\ ATARI  SM124        _    |",
            r" \_____________________________/ ",
            r"   !_________________________!   ",
        ]
        self.horizontal_border = "─"
        self.vertical_border = "│"
        self.upper_right_corner = "┐"
        self.upper_left_corner = "┌"
        self.bottom_left_corner = "└"
        self.bottom_right_corner = "┘"
        self.clipboardManager = ClipboardManager()
        self.browserManager = BrowserManager()
        self.selected_widget = 0

    def open_auth_page(self):
        return self.browserManager.open_browser("https://pongconsole.xyz/dcauth/login")

    async def view(self, app):
        super().view(app)
        height, width = self.window.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, 215, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        y = height // 2 - len(self.message)
        for text in self.message:
            self.window.addstr(
                y,
                width // 2 - len(text) // 2,
                text,
                curses.color_pair(2),
            )
            y += 1

        auth_button = Button(
            height - 25,
            width // 2 - (100 // 2),
            width=100,
            text="Hello stranger, just press enter to register",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            key=keyboard.Key.enter,
            callback=self.open_auth_page,
            selected=True,
        )

        exit_button = Button(
            height - 15,
            width // 2 - (45 // 2),
            width=45,
            text="End before it even began...",
            text_color_pair_id=6,
            frame_color_pair_id=5,
            key=keyboard.Key.enter,
            go_to=AppState.MAIN_MENU,
        )

        self.input_manager = app.input_manager
        self.widgets = [auth_button, exit_button]
        self.register_input_managers(*self.widgets)
        self.refresh()

        res = None
        while True:
            if res := self.refresh():
                break
            clip = self.clipboardManager.get_clipboard()
            if re.match(r"^[a-fA-F0-9]{64}$", clip):
                app.TOKEN = clip
                return AppState.MAIN_MENU
            curses.doupdate()
            await asyncio.sleep(0.08)
        return res

    def press_on(self, key):
        if key == keyboard.Key.up:
            self.widgets[self.selected_widget].selected = False
            if not self.selected_widget == 0:
                self.selected_widget -= 1
            else:
                self.selected_widget = len(self.widgets) - 1

            self.widgets[self.selected_widget].selected = True

        elif key == keyboard.Key.down:
            self.widgets[self.selected_widget].selected = False

            if not self.selected_widget == len(self.widgets) - 1:
                self.selected_widget += 1
            else:
                self.selected_widget = 0

            self.widgets[self.selected_widget].selected = True

        elif key == keyboard.Key.enter:
            if self.selected_widget == 1:
                self.widgets[self.selected_widget].toggle()
            elif self.selected_widget == 0:
                self.open_auth_page()


auth = Auth()
