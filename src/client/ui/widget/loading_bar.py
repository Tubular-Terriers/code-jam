import curses
import sys
import time

# Fix later
try:
    from .Widget import Widget
except Exception:
    from Widget import Widget


class LoadingBar(Widget):
    def __init__(self, width, y, x, message=None):
        super().__init__("loading bar")
        self.height = 5
        self.width = width
        self.y = y
        self.x = x
        self.message = message
        self.win = curses.newwin(self.height, self.width, self.y, self.x)
        self.window = self.win
        self.progress = 0

    def update(self):
        self.win.erase()
        x = int(self.progress)
        x = x / 10
        x = int(x)
        display = "\n┌──────────┐\n│" + "#" * x + "-" * (10 - x) + "│\n└──────────┘"
        if self.message is not None:
            display = self.message + display
        self.win.addstr(0, 1, f"{display}")
        self.win.refresh()

    def set_progress(self, progress: float):
        self.progress = progress

    def refresh(self):
        self.update()


if __name__ == "__main__":
    curses.initscr()
    a = LoadingBar(width=32, y=0, x=0)
    loading = 0
    while loading < 100:
        loading += 1
        time.sleep(0.3)
        a.set_progress(loading)
        a.refresh()
