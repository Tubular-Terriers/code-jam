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
        self.message_text = "\n███▀▀▀██ ███▀▀▀███ ███▀█▄█▀███ ██▀▀▀\n██    ██ ██     ██ ██   █   ██ ██   \n██   ▄▄▄ ██▄▄▄▄▄██ ██   ▀   ██ ██▀▀▀\n██    ██ ██     ██ ██       ██ ██   \n███▄▄▄██ ██     ██ ██       ██ ██▄▄▄\n                                    \n███▀▀▀███ ▀███  ██▀ ██▀▀▀ ██▀▀▀▀██▄ \n██     ██   ██  ██  ██    ██     ██ \n██     ██   ██  ██  ██▀▀▀ ██▄▄▄▄▄▀▀ \n██     ██   ██  █▀  ██    ██     ██ \n███▄▄▄███    ▀█▀    ██▄▄▄ ██     ██▄\n"    
        # print(self.message)

    async def view(self, app):
        # Required
        super().view(app)
        self.window.addstr(0, 1, f"{self.message_text}")
        self.refresh()
        
    def main_menu_r(self):
        pass

game_over = Game_over()