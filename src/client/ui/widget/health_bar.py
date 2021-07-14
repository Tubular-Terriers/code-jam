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

curses.initscr()


class health_bar(Widget):
    def __init__(self, health, message=None):
        super().__init__("health bar")
        self.height = 5
        self.width = 35
        self.y = 0
        self.x = curses.COLS - 35
        self.message = message
        self.max_health = health
        self.health = health
        self.window = curses.newwin(self.height, self.width, self.y, self.x)

    def refresh(self):
        self.window.erase()
        display = (
            "\n┌──────────┐\n│"
            + " " * (self.max_health - self.health)
            + "♡" * self.health
            + "│\n└──────────┘"
        )
        self.window.addstr(1, self.max_health - self.health, f"{display}")
        if self.message is not None:
            self.message = " " * (self.max_health - len(self.message)) + self.message
            self.window.addstr(1, 1, self.message)
        self.window.refresh()

    def set_health(self, minus_health):
        x = self.health - minus_health
        self.health = x
        self.refresh()


if __name__ == "__main__":
    curses.initscr()
    a = health_bar(10)
    loading = 0
    while loading < 9:
        loading += 1
        time.sleep(1)
        a.set_health(1)
        a.refresh()

        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("c"):
            raise KeyboardInterrupt
