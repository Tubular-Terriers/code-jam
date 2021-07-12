# base class for all windows
import curses

# import os

# print(os.path.dirname(os.path.abspath(".")))

# def clamp(lower, value, upper):
#     return max(lower, min(value, upper))

# DEFAULT_HEIGHT = 10
# DEFAULT_WIDTH = 100


class UI:
    """Base class for all ui's"""

    def __init__(self, name):
        self.name = name
        # use this for setting widgets for now
        self.widgets = []

    def view(self, app):
        """
        Opens inside an Application

        app: Application object
        """
        h = app.screen.getmaxyx()[0]
        w = app.screen.getmaxyx()[1]
        self.window = curses.newwin(h, w, 0, 0)

    def key_press_on(self, k):
        """
        `on_press_key` but backwards

        default behavior is to loop all widgets
        """
        for w in self.widgets:
            w.key_press_on(k)

    def refresh(self):
        self.window.refresh()
        for w in self.widgets:
            w.refresh()
