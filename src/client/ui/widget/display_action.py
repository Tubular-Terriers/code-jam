import curses
from enum import Enum

# Fix later
try:
    from ._widget import Widget
except ImportError:
    from _widget import Widget
# Debug only imports
import time

import keyboard


class Display_action(Widget):
    def __init__(self, message=""):
        super().__init__("action display")
        self.message = message
        self.height = 4
        self.width = 30
        self.y = 1
        self.x = curses.COLS - 31
        self.win = curses.newwin(self.height, self.width, self.y, self.x)

    def view(self):
        self.win.erase()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.win.attron(curses.A_ITALIC)
        self.win.attron(curses.color_pair(2))
        self.message = "--<" + self.message + ">--"
        self.win.addstr(1, 0, f"{self.message}")
        self.win.refresh()
        self.win.attroff(curses.A_ITALIC)
        self.win.attroff(curses.color_pair(2))


if __name__ == "__main__":
    curses.initscr()
    a = Display_action("you killed josh")
    a.view()
    time.sleep(2)
