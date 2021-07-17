import asyncio
import os
import sys
import time
from time import sleep
from types import SimpleNamespace

from client.input.input_manager import input_manager
from client.ui.auth import auth
from client.ui.credits import credits_scr
from client.ui.error_sc import ss_error
from client.ui.game_over import game_over
from client.ui.main_menu import main_menu
from client.ui.host_scr import host_game
from client.ui.menu import menu
from client.ui.settings import settings

sys.path.append(".")
import curses

from client.appstate import AppState


class App:
    """
    Static class for app

    Every UI is mounted here
    """

    def __init__(self, stdscr=None):
        self.state = AppState.AUTH_SCR  # temp
        # self.state = AppState.MAIN_MENU

        # FIXME Change this later
        self.target_height = 30
        self.target_width = 130

        self.valid = True

        if not stdscr:
            li = os.get_terminal_size().lines
            c = os.get_terminal_size().columns
            if li < self.target_height or c < self.target_width:
                print("window is not big enough")
                print(
                    f"expected {self.target_height}x{self.target_width}, got {li}x{c}"
                )
                self.valid = False
                return

            stdscr = curses.initscr()
            curses.start_color()
            curses.endwin()

        # Register colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

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
        self.ui.main_menu = main_menu
        self.ui.game_over = game_over
        self.ui.ss_error = ss_error  # TODO: Remove or use this
        self.ui.credit = credits_scr
        self.ui.settings = settings
        self.ui.auth = auth
        self.ui.host_game = host_game

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
        if not self.valid:
            return
            # Run a custom curses error screen maybe
        while True:  # To-do check this.
            if (
                self.stdscr.getmaxyx()[0] < self.target_height
                or self.stdscr.getmaxyx()[1] < self.target_width
            ):  # Allow smaller screen temporarily
                await self.set_ui(ss_error)
                try:
                    curses.resize_term(self.target_height, self.target_width)
                except Exception:  # noqa: S110
                    pass
            elif self.state == AppState.MENU:
                self.state = await self.set_ui(self.ui.menu)
            elif self.state == AppState.MAIN_MENU:
                self.state = await self.set_ui(self.ui.main_menu)
            elif self.state == AppState.GAME:
                # TO-Do
                break
            elif self.state == AppState.GAME_OVER:
                self.state = await self.set_ui(self.ui.game_over)
            elif self.state == AppState.CREDITS_SCR:
                self.state = await self.set_ui(self.ui.credit)
            elif self.state == AppState.SETTINGS_SCR:
                self.state = await self.set_ui(self.ui.settings)
            elif self.state == AppState.AUTH_SCR:
                self.state = await self.set_ui(self.ui.auth)
            elif self.state == AppState.HOST_GAME:
                self.state = await self.set_ui(self.ui.host_game)
            elif self.state == AppState.EXIT:
                break
            else:
                break
        self.destroy()

    def refresh(self):
        """Refreshes everything by cascading"""
        self.selected_ui.refresh()


app = App()
