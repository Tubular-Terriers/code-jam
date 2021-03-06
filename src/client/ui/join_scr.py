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


class Join_game_scr(UI):
    """defines the ui screen when the player wants to join a game"""

    def __init__(self):
        super().__init__("join game")
        self.message = [
            "JOIN A GAME",
            "Please enter your code below to join the game.",
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

        y += 1

        w = 10
        textbox = Box(
            3,
            15,
            (height // 2) + y,
            width // 2 - w // 2 - 2,
        )
        y += 4
        play_button = Button(
            (height // 2) + y,
            (width - 30) // 2 - 5,
            text="Start game",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            width=15,
            go_to=AppState.GAME,
            key=keyboard.Key.enter,
            selected=self.selected_widget == 1,
        )
        exit_button = Button(
            (height // 2) + y,
            (width - 30) // 2 + 20,
            text="Back",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            width=15,
            go_to=AppState.MAIN_MENU,
            key=keyboard.Key.enter,
            selected=self.selected_widget == 2,
        )

        self.widgets = [textbox, play_button, exit_button]
        self.refresh()
        self.input_manager = app.input_manager
        self.register_input_managers(*self.widgets)
        while True:
            if res := self.refresh():
                app.game_code = textbox.text
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
            if self.selected_widget >= 1:
                self.widgets[self.selected_widget].toggle()
            else:
                self.widgets[self.selected_widget].press_on(key)
        elif self.selected_widget == 0:
            self.widgets[self.selected_widget].press_on(key)


join_game = Join_game_scr()
