import asyncio
import sys
from types import SimpleNamespace

from input.input_manager import input_manager
from ui.menu import menu

sys.path.append(".")
import curses

from appstate import AppState


class App:
    """
    Static class for app

    Every UI is mounted here
    """

    def __init__(self, stdscr=None):
        self.state = AppState.MENU

        if not stdscr:

            stdscr = curses.initscr()
        self.stdscr = stdscr
        self.screen = stdscr

        # FIXME remove this in self.destroy
        curses.noecho()
        curses.nocbreak()
        curses.curs_set(0)
        curses.raw()

        # Register UIs
        self.ui = SimpleNamespace()
        self.ui.menu = menu

        # Register input_manager
        self.input_manager = input_manager

        # No longer a function since we moved to pynput
        # def hook(e):
        #     self.selected_ui.hook(e)

        # self.hook = hook
        # self.input_manager.hook(hook)

        def press_on(e):
            # FIXME find a way to disable curses input buffer
            curses.flushinp()
            self.selected_ui.press_on(e)

        def release_on(e):
            self.selected_ui.release_on(e)

        def start_text_on(e):
            self.selected_ui.start_text_on(e)

        def update_text_on(e):
            # FIXME find a way to disable curses input buffer
            curses.flushinp()
            self.selected_ui.update_text_on(e)

        def end_text_on(e):
            self.selected_ui.end_text_on(e)

        self.input_manager.on_press(press_on)
        self.input_manager.on_release(release_on)
        self.input_manager.on_text_start(start_text_on)
        self.input_manager.on_text_update(update_text_on)
        self.input_manager.on_text_end(end_text_on)

        menu.input_manager = self.input_manager

    def destroy(self):
        """Cleans up the resources"""
        # Release keyboard hook
        # No longer a function
        # self.input_manager.unhook(self.hook)

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
