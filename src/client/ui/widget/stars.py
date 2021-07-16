import curses
import random
import time

from ._widget import Widget


class Stars(Widget):
    def __init__(self, height, width):
        super().__init__("stars")
        self.window = curses.newwin(height, width, 0, 0)
        self.height = height
        self.width = width
        self.locations_x = []
        self.locations_y = []
        self.stars = ["✶", "*"]
        self.refreshtime = 0
        for _ in range(250):
            self.locations_x.append(random.randint(0, self.width - 1))
            self.locations_y.append(random.randint(0, self.height - 1))

    def refresh(self):
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
