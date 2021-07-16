import asyncio
import curses
import random

from pynput import keyboard

from client.appstate import AppState

from ._ui import UI
from .widget.button import Button
from .widget.progress_bar import ProgressBar
from .widget.simple_textbox import Box


class Settings(UI):
    def __init__(self):
        super().__init__("setings_screen")

    async def veiw(self, app):
        pass
        return True


settings = Settings()
