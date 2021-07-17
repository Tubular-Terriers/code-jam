import curses
import time

from pynput import keyboard
from ._widget import Widget


class password(Widget):
    """The widget for making a text box to get a password"""

    def __init__(self, h, w, y, x):
        super().__init__("text box")
        self.window = curses.newwin(h, w, y, x)
        self.text = "enter"
        self.accept = False
        self.typing = False

    def refresh(self):
        self.window.erase()
        self.window.border(0)
        self.window.addstr(1, 1, "*")
        if self.typing:
            self.window.addstr(2, 1, "TYPING")
        self.window.noutrefresh()

    def press_on(self, key):
        if key == keyboard.Key.enter:
            self.input_manager.trigger_input()
            self.typing = True

    def start_text_on(self, *_):
        self.typing = True
        self.refresh()
        curses.doupdate()

    def update_text_on(self, text, *_):
        if text is None:
            self.text = "enter your password"
            self.refresh()
            curses.doupdate()
            return
        if len(text) > 10:
            self.input_manager.set_text(text[:10])
        self.text = text[:10]
        self.window.refresh()

    def end_text_on(self, *_):
        self.typing = False
