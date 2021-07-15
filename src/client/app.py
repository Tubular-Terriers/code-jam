import asyncio
import sys
import time
from time import sleep
from types import SimpleNamespace

from client.input.input_manager import input_manager
from client.ui.error_sc import ss_error
from client.ui.game_over import game_over
from client.ui.main_menu import main_menu
from client.ui.menu import menu

sys.path.append(".")
import curses

from client.appstate import AppState


class App:
    """
    Static class for app

    Every UI is mounted here
    """

    def __init__(self, stdscr=None):
        self.state = AppState.MAIN_MENU  # temp

        if not stdscr:

            stdscr = curses.initscr()
            curses.start_color()

        # Register colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

        self.stdscr = stdscr
        self.screen = stdscr
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        # FIXME remove this in self.destroy
        curses.noecho()
        curses.nocbreak()
        curses.curs_set(0)
        curses.raw()

        # Register UIs
        self.ui = SimpleNamespace()
        self.ui.menu = menu
        self.ui.main_menu = main_menu
        self.ui.game_over = game_over
        self.ui.ss_error = ss_error

        # Register input_manager
        self.input_manager = input_manager

        # No longer a function since we moved to pynput
        # def hook(e):
        #     self.selected_ui.hook(e)

        # self.hook = hook
        # self.input_manager.hook(hook)

        def press_on(e):
            self.selected_ui.press_on(e)

        def release_on(e):
            self.selected_ui.release_on(e)

        def start_text_on(e):
            self.selected_ui.start_text_on(e)

        def update_text_on(e):
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

        curses.endwin()  # ending curses window(terminal problem in linux)

    async def set_ui(self, ui):
        self.selected_ui = ui
        return await ui.view(self)

    async def run(self):
        while True:  # To-do check this.
            if self.screen_height < 20 or self.screen_width < 130: #if doesnt work in your terminal, change these numbers
                await self.set_ui(ss_error)
            elif self.state == AppState.MENU:
                self.state = await self.set_ui(self.ui.menu)
            elif self.state == AppState.MAIN_MENU:
                self.state = await self.set_ui(self.ui.main_menu)
            elif self.state == AppState.GAME:
                # TO-Do
                break
            elif self.state == AppState.GAME_OVER:
                self.state = await self.set_ui(self.ui.game_over)
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
