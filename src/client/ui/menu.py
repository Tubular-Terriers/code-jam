import asyncio
import curses
import time
from time import sleep

from appstate import AppState

from ._ui import UI
from .widget.progress_bar import ProgressBar
from .widget.simple_button import Button
from .widget.simple_textbox import Box


class Menu(UI):
    def __init__(self):
        super().__init__("menu screen")
        self.time = 0

    async def view(self, app):
        # Required
        super().view(app)
        self.time += 10
        my_bar = ProgressBar(
            width=32, y=1, x=0, message_text="Press space 4 times to exit"
        )
        my_bar.set_progress(self.time)
        my_button = Button(2, 14, go_to=AppState.EXIT)
        editor = Box(3, 20)
        # You can manually refresh them as well
        self.widgets = [my_bar, my_button, editor]
        res = None
        i = 0
        while True:
            # Main loop for rendering the menu
            i += 1
            self.window.addstr(0, 0, f"I am a menu {i}")
            my_bar.set_progress(i % 100)
            if res := self.refresh():
                break
            curses.doupdate()
            await asyncio.sleep(0.1)
        return res


# Return single menu object
menu = Menu()
