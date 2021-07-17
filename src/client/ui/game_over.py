import asyncio
import curses
import time
from time import sleep

from pynput import keyboard

from client.appstate import AppState

from ._ui import UI
from .widget.button import Button
from .widget.progress_bar import ProgressBar
from .widget.simple_textbox import Box


class Game_over(UI):
    """defines the game over screen"""

    def __init__(self):
        super().__init__("game_over_scr")
        self.position = "1"
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
        self.message_text12 = " you came #" + self.position + ", better luck next time."
        # print(self.message)
        self.selected_widget = 0

    async def view(self, app):
        # Required
        super().view(app)
        height, width = self.window.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
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
        self.window.addstr(
            int((height / 2) + 4),
            int(width / 2) - 15,
            f"{self.message_text12}",
            curses.color_pair(1),
        )
        self.refresh()
        menu_button = Button(
            (height // 2) + 6,
            width // 2 + 10,
            text="Main menu",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            width=15,
            go_to=AppState.MAIN_MENU,
            key=keyboard.Key.enter,
            selected=self.selected_widget == 0,
        )
        exit_button = Button(
            (height // 2) + 6,
            width // 2 + 5,
            text="Exit",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            width=15,
            go_to=AppState.EXIT,
            key=keyboard.Key.enter,
            selected=self.selected_widget == 1,
        )

        self.input_manager = app.input_manager
        self.widgets = [menu_button, exit_button]
        self.refresh()

        while True:
            if res := self.refresh():
                break
            curses.doupdate()
            await asyncio.sleep(0.08)
        return res

    def press_on(self, key):
        if key == keyboard.Key.left:
            self.widgets[self.selected_widget].selected = False
            if not self.selected_widget == 0:
                self.selected_widget -= 1
            else:
                self.selected_widget = len(self.widgets) - 1
            self.widgets[self.selected_widget].selected = True

        elif key == keyboard.Key.right:
            self.widgets[self.selected_widget].selected = False
            if not self.selected_widget == len(self.widgets) - 1:
                self.selected_widget += 1
            else:
                self.selected_widget = 0

            self.widgets[self.selected_widget].selected = True

        elif key == keyboard.Key.enter:
            self.widgets[self.selected_widget].toggle()


game_over = Game_over()
