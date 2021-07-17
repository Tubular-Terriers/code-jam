import asyncio
import curses
import random

from pynput import keyboard

from client.appstate import AppState

from ._ui import UI
from .widget.button import Button
from .widget.progress_bar import ProgressBar
from .widget.slider import Orientation, Slider


class Settings(UI):
    def __init__(self):
        super().__init__("settings_screen")
        self.title = [
            "  ____        _    _    _                    ",
            " / ___|  ___ | |_ | |_ (_) _____  ____  ___  ",
            " \___ \ / _ \| __|| __|| ||  _  \/ _  |/ __| ",
            "  ___) |  __/| |_ | |_ | || | | ||(_| |\__ \ ",
            " |____/ \___| \__||\__||_||_| |_|\__, ||___/ ",
            "                                 |___/       ",
        ]
        self.height = 0
        self.width = 0
        self.selected_widget = 0
        self.increment = 10
        self.increment_slider = None

    async def view(self, app):
        super().view(app)
        self.height, self.width = self.window.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, 215, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.window.attron(curses.color_pair(2))

        y = 0
        for text in self.title:
            self.window.addstr(
                self.height // 5 - len(self.title) + y,
                self.width // 2 - len(text) // 2,
                text,
                curses.color_pair(2),
            )
            y += 1

        self.window.attroff(curses.color_pair(2))
        self.window.attron(curses.A_NORMAL)

        width = 25
        previous_menu_button = Button(
            self.height - self.height // 5,
            self.width // 2 - (width // 2),
            text_color_pair_id=4,
            frame_color_pair_id=5,
            width=width,
            text="Back",
            key=keyboard.Key.enter,
            go_to=AppState.MAIN_MENU,
            selected=self.selected_widget == 0,
        )

        save_button = Button(
            previous_menu_button.y - 4,
            self.width // 2 - (width // 2),
            text_color_pair_id=4,
            frame_color_pair_id=5,
            width=width,
            text="Save",
            key=keyboard.Key.enter,
            go_to=AppState.MAIN_MENU,
            selected=self.selected_widget == 1,
        )

        apply_button = Button(
            save_button.y - 4,
            self.width // 2 - (width // 2),
            text_color_pair_id=4,
            frame_color_pair_id=5,
            width=width,
            text="Apply",
            key=keyboard.Key.enter,
            go_to=AppState.MAIN_MENU,
            selected=self.selected_widget == 2,
        )

        width = 4
        height = 20
        self.increment_slider = Slider(
            self.height // 2 - (height // 2),
            self.width - width - 15,
            text="UP/DOWN",
            frame_color_pair_id=5,
            height=height,
            width=width,
            selected=self.selected_widget == 3,
            orientation=Orientation.VERTICAL,
        )

        width = 55
        sfx_volume_slider = Slider(
            self.height // 2 - (height // 2),
            self.width // 2 - (width // 2),
            text="LEFT/RIGHT",
            text_color_pair_id=4,
            frame_color_pair_id=5,
            progress_color_pair_id=3,
            progress_left_color_pair_id=7,
            width=width,
            selected=False,  # self.selected_widget == 2 FIXME
            progress=50,
        )

        music_volume_slider = Slider(
            self.height // 2 - (height // 2) + 7,
            self.width // 2 - (width // 2),
            text="LEFT/RIGHT",
            text_color_pair_id=4,
            frame_color_pair_id=5,
            progress_color_pair_id=3,
            progress_left_color_pair_id=7,
            width=width,
            selected=False,  # self.selected_widget == 2 FIXME
            progress=50,
        )

        self.widgets = [
            previous_menu_button,
            save_button,
            apply_button,
            self.increment_slider,
            sfx_volume_slider,
            music_volume_slider,
        ]
        self.refresh()

        while True:
            if res := self.refresh():
                break
            self.update()
            curses.doupdate()
            await asyncio.sleep(0.1)
        return res

    def draw_text(self, active_text):
        self.window.addstr(
            self.height // 2 + (height // 2), self.width - width - 16, "Set increment"
        )

        txt = "Sound Effects Volume"
        self.window.addstr(
            self.height // 2 - (height // 2) + 6, self.width // 2 - (len(txt) // 2), txt
        )

        txt = "Music volume"
        self.window.addstr(
            self.height // 2 - (height // 2) + 13,
            self.width // 2 - (len(txt) // 2),
            txt,
        )

    def update(self):
        self.increment = self.increment_slider.progress

    def press_on(self, key):
        if self.selected_widget == 0:
            if key == keyboard.Key.enter:
                self.widgets[self.selected_widget].toggle()


settings = Settings()
