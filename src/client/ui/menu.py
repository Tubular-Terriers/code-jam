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


class Menu(UI):
    """use for testing"""

    def __init__(self):
        super().__init__("menu screen")
        self.time = 0

    async def view(self, app):
        # Required
        super().view(app)
        self.time += 10
        my_bar = ProgressBar(width=32, y=1, x=0, message_text="Press space to exit")
        my_bar.set_progress(self.time)
        my_button = Button(2, 34, go_to=AppState.GAME_OVER)
        editor = Box(3, 20, 5, 0)
        # You can manually refresh them as well
        self.widgets = [my_bar, my_button, editor]
        self.input_manager = app.input_manager
        self.register_input_managers(
            *self.widgets
        )  # Give them access to the input_manager
        res = None
        i = 0
        while True:
            # Main loop for rendering the menu
            i += 1
            self.window.addstr(
                0,
                0,
                f"I am a menu {i} - is 'i' pressed? {'yes' if self.input_manager.is_pressed('i') else 'no '}",
            )
            my_bar.set_progress(i % 100)
            if res := self.refresh():
                break
            curses.doupdate()
            await asyncio.sleep(0.1)
        return res


# Return single menu object
menu = Menu()
