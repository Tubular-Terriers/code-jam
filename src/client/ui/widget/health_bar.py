import curses
import time

curses.initscr()


class health_bar:
    def __init__(self, health, message=None):
        self.height = 5
        self.width = 35
        self.y = 0
        self.x = curses.COLS - 35
        self.message = message
        self.max_health = health
        self.health = health
        self.win = curses.newwin(self.height, self.width, self.y, self.x)

    def update(self):
        self.win.erase()
        display = (
            "\n┌──────────┐\n│"
            + " " * (self.max_health - self.health)
            + "♡" * self.health
            + "│\n└──────────┘"
        )
        if self.health != 0:
            self.win.addstr(1, self.max_health - self.health, f"{display}")
        if self.message is not None:
            self.message = " " * (self.max_health - len(self.message)) + self.message
            self.win.addstr(1, 1, self.message)
        self.win.refresh()

    def set_health(self, minus_health):
        x = self.health - minus_health
        self.health = x
        self.update()
