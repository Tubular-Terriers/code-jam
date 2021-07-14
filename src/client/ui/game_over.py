import asyncio
import curses
import time
from time import sleep

from appstate import AppState
from pynput import keyboard

from ._ui import UI
from .widget.progress_bar import ProgressBar
from .widget.simple_button import Button
from .widget.simple_textbox import Box


class Game_over(UI):
    def __init__(self):
        super().__init__("game_over_scr")

    async def view(self):
        pass

    def main_menu_r(self):
        pass

    def _create_message_(self) -> str:
        pass


# instanciate object from game_over class
game_over = Game_over()


if __name__ == "__main__":
    curses.initscr()
