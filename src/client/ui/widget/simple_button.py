import curses
import sys
import time

from pynput import keyboard

from ._widget import Widget


class Button(Widget):
    """
    A simple widget to get a input button.

    For eg, if the key esc is asigned to it and a appstate,
    it will change the appstate to it when the esc key is pressed
    """

    def __init__(self, y, x, toggled=False, key=keyboard.Key.space, go_to=None):
        super().__init__("button")
        self.window = curses.newwin(3, 3, y, x)
        self.toggled = toggled
        self.toggle_count = 0
        self.key = key
        self.go_to = go_to

    def refresh(self):
        self.window.border(0)
        self.window.addch(1, 1, "o" if self.toggled else "x")
        self.window.noutrefresh()
        if self.toggle_count >= 1:
            if self.go_to is not None:
                return self.go_to

    def press_on(self, key):
        if key == self.key or key.char == self.key:
            self.toggle_count += 1
            self.toggled = not self.toggled
