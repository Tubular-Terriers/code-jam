import asyncio
import sys
from types import SimpleNamespace

from input.input_manager import input_manager
from ui.menu import menu

sys.path.append(".")
from appstate import AppState


class App:
    """
    Static class for app

    Every UI is mounted here
    """

    def __init__(self, stdscr=None):
        self.state = AppState.MENU

        if not stdscr:
            import curses

            stdscr = curses.initscr()
        self.stdscr = stdscr
        self.screen = stdscr

        curses.noecho()

        # Register UIs
        self.ui = SimpleNamespace()
        self.ui.menu = menu

        # Register input_manager
        self.input_manager = input_manager

        def hook(e):
            self.selected_ui.hook(e)

        self.hook = hook
        self.input_manager.hook(hook)

        def press_on(e):
            self.selected_ui.press_on(e)

        self.input_manager.on_press(press_on)

    def destroy(self):
        """Cleans up the resources"""
        # Release keyboard hook
        self.input_manager.unhook(self.hook)

    async def set_ui(self, ui):
        self.selected_ui = ui
        return await ui.view(self)

    async def run(self):
        while True:
            if self.state == AppState.MENU:
                self.state = await self.set_ui(self.ui.menu)
            elif self.state == AppState.EXIT:
                break
            else:
                break
            await asyncio.sleep(1)
        self.destroy()

    def refresh(self):
        """Refreshes everything by cascading"""
        self.selected_ui.refresh()


app = App()
