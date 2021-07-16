import asyncio
import curses
import random
import re

from pynput import keyboard

from client.appstate import AppState
from client.tools.clipboard import ClipboardManager
from client.tools.browser import BrowserManager
from ._ui import UI
from .widget.button import Button


class Auth(UI):
    """makes main screen ui"""

    def __init__(self):
        super().__init__("main_menu_scr")
        self.message = [
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@@@@*/(@@@@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@@%%%%%%,@@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@(  *% ,%#@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@@#%  %(%@@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@%% . ..%%@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@#*, //@%%%%%%%%/* *@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@*      ////@@@. @@@///     #@@@@@@@@@@@",
            "@@@@@@@@@@@        ////@@  @@//,       *@@@@@@@@@@",
            "@@@@@@@@@@@*      *  ///@   ///        (@@@@@@@@@@",
            "@@@@@@@@@@@.     # /%%,.  @@%%%         @@@@@@@@@@",
            "@@@@@@@@@@@     .%#%        &          ,@@@@@@@@@@",
            "@@@@@@@@@@@@        .     &       ,   *@@@@@@@@@@@",
            "@@@@@@@@@@@@@@*,          .*         ,@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@             @@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@..,**//((##%%@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        ]
        self.horizontal_border = "─"
        self.vertical_border = "│"
        self.upper_right_corner = "┐"
        self.upper_left_corner = "┌"
        self.bottom_left_corner = "└"
        self.bottom_right_corner = "┘"
        self.clipboardManager = ClipboardManager()
        self.browserManager = BrowserManager()

    def select_widget(self, widget_id):
        pass

    def open_auth_page(self):
        return self.browserManager.open_browser("https://pongconsole.xyz/dcauth/login")

    async def view(self, app):
        # prints the text of the screen
        # Required
        super().view(app)
        height, width = self.window.getmaxyx()

        y = 0

        for text in self.message:
            self.window.addstr(
                y,
                width // 2 - len(text) // 2,
                text,
                curses.color_pair(2),
            )
            y += 1

        auth_button = Button(
            len(self.message) + 5,
            (width - 150) // 2,
            width=150,
            text="Wait! If you have a TOKEN, just copy it and my guy will know that; if not GET THE HE... No, you're welcome. Just press enter to register...",
            text_color_pair_id=5,
            frame_color_pair_id=5,
            key=keyboard.Key.enter,
            callback=self.open_auth_page,
        )

        exit_button = Button(
            len(self.message) + auth_button.height + 5,
            (width - 25) // 2,
            width=25,
            text="end before it began...",
            text_color_pair_id=5,
            frame_color_pair_id=5,
            key=keyboard.Key.enter,
            go_to=AppState.EXIT
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
                print(clip)
                return AppState.MAIN_MENU
            curses.doupdate()
            await asyncio.sleep(0.08)
        return res


auth = Auth()
