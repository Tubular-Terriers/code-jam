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
        self.input_manager = None

    def view(self, app):
        """
        Opens inside an Application

        app: Application object
        """
        h = app.screen.getmaxyx()[0]
        w = app.screen.getmaxyx()[1]
        self.window = curses.newwin(h, w, 0, 0)

    def register_input_managers(self, *args):
        for w in args:
            w.input_manager = self.input_manager

    def press_on(self, k):
        """
        `on_press` but backwards

        default behavior is to loop all widgets
        """
        for w in self.widgets:
            w.press_on(k)

    def release_on(self, k):
        """
        `on_press` but backwards

        default behavior is to loop all widgets
        """
        for w in self.widgets:
            w.release_on(k)

    # Text related methods
    def start_text_on(self, k):
        for w in self.widgets:
            w.start_text_on(k)

    def update_text_on(self, k):
        for w in self.widgets:
            w.update_text_on(k)

    def end_text_on(self, k):
        for w in self.widgets:
            w.end_text_on(k)

    # Deprecated
    def hook(self, key):
        pass

    def refresh(self):
        """Default behavior. Recommended that you change it"""
        self.window.refresh()
        for w in self.widgets:
            if (res := w.refresh()) is not None:
                return res
