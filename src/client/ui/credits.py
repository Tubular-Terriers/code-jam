import asyncio
import curses
import random

from pynput import keyboard

from client.appstate import AppState

from ._ui import UI
from .widget.progress_bar import ProgressBar
from .widget.simple_button import Button
from .widget.simple_textbox import Box
from .widget.stars import Stars


class Credits(UI):
    def __init__(self):
        super().__init__("main_menu_scr")
        self.spacing = 3
        self.button_text = "Press Space to go to back to game menu"
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
        self.refreshtime = 0
        

    async def view(self, app):
        # Required
        super().view(app)
        height, width = self.window.getmaxyx()
        for _ in range(250):
            self.locations_x.append(random.randint(0, width - 1))
            self.locations_y.append(random.randint(0, height - 1))
        print(height, width)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        star_background = Stars(height, width)
        y = 17
        menu_button = Button(
            height // 3 + y + self.spacing - 1,
            (width // 2) - len(self.button_text) // 2 - 3,
            key=keyboard.Key.space,
            go_to=AppState.MAIN_MENU,
        )

        self.input_manager = app.input_manager
        self.widgets = [menu_button]
        self.register_input_managers(*self.widgets)
        res = None
        while True:
            if self.refreshtime % 10 == 0:
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
            self.refreshtime += 1
            curses.doupdate()
            self.window.attron(curses.color_pair(2))
            self.window.attron(curses.A_BOLD)
            y = 0
            for text in self._credits_:
                self.window.addstr(height // 3 + y, width // 2 - len(text) // 2, text)
                y += 1

            self.window.attron(curses.A_ITALIC)

            color_id = 1
            for nick in self.devs:

                if color_id % 2 == 0:
                    self.window.attron(curses.color_pair(3))
                else:
                    self.window.attron(curses.color_pair(4))

                self.window.addstr(
                    height // 3 + y + self.spacing - 1,
                    width // 2 - len(nick) // 2,
                    nick,
                )
                y += 2
                color_id += 1

            self.window.attroff(curses.color_pair(2))
            self.window.attroff(curses.A_BOLD)

            self.window.addstr(
                height // 3 + y + self.spacing,
                (width // 2) - len(self.button_text) // 2,
                self.button_text,
            )
            self.window.refresh()
            
            if res := self.refresh():
                break
            await asyncio.sleep(0.1)
        return res
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


credits_scr = Credits()
