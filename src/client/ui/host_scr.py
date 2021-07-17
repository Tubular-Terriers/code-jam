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


class Host_game_scr(UI):
    """defines the ui screen when the player wants to host a game"""

    def __init__(self):
        super().__init__("host game")
        self.game_code = "#code#"
        self.message = [
            "Please ask the others to join using the following method:",
            "1. click the join a game.",
            "2. enter your game code: " + self.game_code,
        ]
        self.player_list = [
            "The players that have joined by now:",
            "nobalpha",
            "pritansh",
            "mephew",
            "karthik",
        ]
        self.selected_widget = 0

    async def view(self, app):
        # Required
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

        y = -1
        for text in self.message:
            self.window.addstr(
                height // 2 - len(self.message) + y,
                width // 2 - len(text) // 2,
                text,
                curses.color_pair(1),
            )
            y += 1
        y += 4
        color_id = 1

        for text2 in self.player_list:
            if color_id % 2 == 0:
                self.window.attron(curses.color_pair(3))
            else:
                self.window.attron(curses.color_pair(4))
            self.window.addstr(
                height // 2 - len(self.player_list) + y,
                width // 2 - len(text2) // 2,
                text2,
                curses.color_pair(1),
            )
            color_id += 1
            y += 1
        play_button = Button(
            (height // 2) + y,
            (width - 30) // 2 - 5,
            text="start game",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            width=15,
            go_to=AppState.GAME,
            key=keyboard.Key.enter,
            selected=self.selected_widget == 0,
        )
        exit_button = Button(
            (height // 2) + y,
            (width - 30) // 2 + 20,
            text="close lobby",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            width=15,
            go_to=AppState.MAIN_MENU,
            key=keyboard.Key.enter,
            selected=self.selected_widget == 1,
        )

        self.widgets = [play_button, exit_button]
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


host_game = Host_game_scr()
