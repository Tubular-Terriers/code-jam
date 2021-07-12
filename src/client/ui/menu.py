import asyncio
import time
from time import sleep

from _ui.UI import UI
from appstate import AppState

from .widget.loading_bar import LoadingBar


class Menu(UI):
    def __init__(self):
        super().__init__("menu screen")
        self.time = 0

    async def view(self, app):
        # Required
        super().view(app)
        self.time += 10
        my_bar = LoadingBar(width=32, y=3, x=3, message="hello")
        my_bar.set_progress(self.time)
        self.widgets = [my_bar]
        self.window.addstr(0, 0, "I am a menu")
        self.refresh()
        return AppState.MENU


# Return single menu object
menu = Menu()
