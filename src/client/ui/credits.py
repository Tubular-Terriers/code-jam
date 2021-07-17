import asyncio
import curses
import random
import sys

from pynput import keyboard

from client.appstate import AppState

from ._ui import UI
from .widget.button import Button


class Credits(UI):
    """the page for the credits ui"""

    def __init__(self):
        super().__init__("main_menu_scr")
        self.stars_count = 250
        self.spacing = 3
        self._credits_ = [
            r"                          _  _    _          ",
            r"  ____  _____   ____   __| ||_| _| |_   ___ ",
            r" /  __||_  __\_/ __ \ / _  || ||_   _|/  __/",
            r" | |__ |  | \/\  ___// |_| || |  | |  \___ \ ",
            r" \____||__|    \____||_____||_|  |_|  /____/",
        ]
        self.devs = [
            "nopeless",
            "pritansh sahsani",
            "karthikmurakonda",
            "MePhew",
            "nobalpha",
            "Nickhil1737",
        ]
        self.locations_x = []
        self.locations_y = []
        self.stars = ["✶", "*"]
        self.refresh_time = 0
        self.height = 0
        self.width = 0
        self.previous_menu_button = None

    async def view(self, app):
        super().view(app)
        self.height, self.width = self.window.getmaxyx()
        if len(self.locations_x) == 0:
            for _ in range(self.stars_count):
                self.locations_x.append(random.randint(0, self.width - 1))
                self.locations_y.append(random.randint(0, self.height - 2))
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, 215, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        width = 25
        self.previous_menu_button = Button(
            self.height - self.height // 5,
            self.width // 2 - (width // 2),
            text_color_pair_id=4,
            frame_color_pair_id=5,
            width=width,
            text="Back",
            key=keyboard.Key.enter,
            go_to=AppState.MAIN_MENU,
            selected=True,
        )

        self.widgets = [self.previous_menu_button]
        self.draw()
        self.refresh()

        while True:
            if res := self.previous_menu_button.refresh():
                break
            self.draw()
            curses.doupdate()
        return res

    def draw(self):
        if self.refresh_time % 10 == 0:
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
            for i in range(len(self.locations_x)):
                self.add_white_star(self.locations_y[i], self.locations_x[i])
                if i % 10 == 0:
                    chose = random.randint(0, 2)
                    if chose == 0:
                        self.add_white_star(self.locations_y[i], self.locations_x[i])
                    elif chose == 1:
                        self.add_blue_star(self.locations_y[i], self.locations_x[i])
                    elif chose == 2:
                        self.remove_star(self.locations_y[i], self.locations_x[i])
                self.window.noutrefresh()
        self.refresh_time += 1
        curses.doupdate()
        self.window.attron(curses.color_pair(8))
        self.window.attron(curses.A_BOLD)
        y = 0
        for text in self._credits_:
            self.window.addstr(
                self.height // 3 + y, self.width // 2 - len(text) // 2, text
            )
            y += 1

        self.window.attron(curses.A_ITALIC)

        color_id = 1
        for nick in self.devs:

            if color_id % 2 == 0:
                self.window.attron(curses.color_pair(3))
            else:
                self.window.attron(curses.color_pair(4))

            self.window.addstr(
                self.height // 3 + y + self.spacing - 1,
                self.width // 2 - len(nick) // 2,
                nick,
            )
            y += 2
            color_id += 1

        self.window.attroff(curses.color_pair(2))
        self.window.attroff(curses.A_BOLD)
        self.window.refresh()

    def add_blue_star(self, y, x):
        self.window.attron(curses.color_pair(1))
        self.window.addstr(y, x, self.stars[random.randint(0, 1)])
        self.window.attroff(curses.color_pair(1))

    def add_white_star(self, y, x):
        self.window.attron(curses.color_pair(2))
        self.window.addstr(y, x, self.stars[random.randint(0, 1)])
        self.window.attron(curses.color_pair(2))

    def remove_star(self, y, x):
        self.window.addstr(y, x, " ")

    def press_on(self, key):
        if key == keyboard.Key.enter:
            self.widgets[0].toggle()


credits_scr = Credits()
