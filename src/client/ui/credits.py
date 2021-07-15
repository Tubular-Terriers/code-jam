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


class Credits(UI):
    def __init__(self):
        super().__init__("main_menu_scr")

        self.message_text1 = "                          _  _    _          "
        self.message_text2 = "  ____  _____   ____   __| ||_| _| |_   ___ "
        self.message_text3 = " /  __||_  __\_/ __ \ / _  || ||_   _|/  __/"
        self.message_text4 = " | |__ |  | \/\  ___// |_| || |  | |  \___ \ "
        self.message_text5 = " \____||__|    \____||_____||_|  |_|  /____/" 
        self.message_text6 = "" #nopeless
        self.message_text7 = "" #karthikmurakonda
        self.message_text8 = ""#MePhew
        self.message_text9 = ""#pritansh sahsani
        self.message_text10 = ""#nobalpha
        self.message_text11 = ""#Nickhil1737
        
        # print(self.message)

    async def view(self, app):
        # Required
        super().view(app)
        height, width = self.window.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.window.attron(curses.color_pair(2))
        self.window.attron(curses.A_BOLD)
        self.window.addstr(
            int((height / 2) - 7),
            int(width / 2) - 20,
            f"{self.message_text1}",
        )
        self.window.addstr(
            int((height / 2) - 6), int(width / 2) - 20, f"{self.message_text2}"
        )
        self.window.addstr(
            int((height / 2) - 5), int(width / 2) - 20, f"{self.message_text3}"
        )
        self.window.addstr(
            int((height / 2) - 4), int(width / 2) - 20, f"{self.message_text4}"
        )
        self.window.addstr(
            int((height / 2) - 3), int(width / 2) - 20, f"{self.message_text5}"
        )
        self.window.addstr(
            int((height / 2) - 2), int(width / 2) - 20, f"{self.message_text6}"
        )
        self.window.addstr(
            int((height / 2) - 1), int(width / 2) - 20, f"{self.message_text7}"
        )
        self.window.addstr(
            int((height / 2)), int(width / 2) - 20, f"{self.message_text8}"
        )
        self.window.addstr(
            int((height / 2) + 1), int(width / 2) - 20, f"{self.message_text9}"
        )
        self.window.addstr(
            int((height / 2) + 2), int(width / 2) - 20, f"{self.message_text10}"
        )
        self.window.addstr(
            int((height / 2) + 3), int(width / 2) - 20, f"{self.message_text11}"
        )
        self.window.attroff(curses.color_pair(2))
        self.window.attroff(curses.A_BOLD)
        self.refresh()
        menu_button = Button(
            (height // 2) + 5,
            (width // 2) - 20,
            key=keyboard.Key.space,
            go_to=AppState.MAIN_MENU,
        )
        self.window.addstr(
            (height // 2) + 6, (width // 2) - 17, "Press Space to go to Game menu"
        )

        self.input_manager = app.input_manager
        self.widgets = [menu_button]
        self.register_input_managers(*self.widgets)
        self.refresh()
        res = None
        while True:
            if res := self.refresh():
                break
            curses.doupdate()
            await asyncio.sleep(0.1)
        return res

credits = Credits()
