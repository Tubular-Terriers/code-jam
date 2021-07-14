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


class Main_menu(UI):
    def __init__(self):
        super().__init__("main menu")

    async def view(self):
        # ui
        pass

    def main_menu_r(self):
        pass

    def _create_message_(self) -> str:
        pass


main_menu = Main_menu()

if __name__ == "__main__":
    curses.initscr()
