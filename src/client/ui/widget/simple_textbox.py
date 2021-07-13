import curses
import sys
import time
import asyncio

from pynput import keyboard
from ._widget import Widget


class Textbox(Widget):
    def __init__(self, y, x, w, h, title=""):
        super().__init__("textbox")
        self.window = curses.newwin(w, h, y, x)
        self.title = title
        self.listener = keyboard.Listener(
            on_release=self.on_release)
        self.buffer = ""

    def start_listener(self):
        self.listener.start()

    def async_wrapper(self, callback):

        def inner(key):
            temp = asyncio.run(callback(key))
            # key combinations traitement
            if temp == -1:
                self.buffer = self.buffer[:-1]
            else:
                self.buffer += temp
            # print(f"str: {kwargs['_str']}")
            self.print_to_stdout(self.window, self.buffer)
        return inner

    async def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        if key == keyboard.Key.backspace:
            return -1
        try:
            return key.char
        except AttributeError:
            return ""

    def print_to_stdout(stdscr, text):
        stdscr.clear()
        print(text)
        title = "Text Box"
        width = max(len(title), len(text))
        title_lspace = (width - len(title)) // 2
        title_rspace = width - len(title) - title_lspace
        stdscr.addstr(0, 0, f"┌─{'─' * (title_lspace)}{title}{'─' * (title_rspace)}─┐")
        text_lspace = (width - len(text)) // 2
        text_rspace = width - len(text) - text_lspace
        stdscr.addstr(1, 0, f"│ {' ' * ( text_lspace)}{text}{' ' * ( text_rspace)} │")
        stdscr.addstr(2, 0, f"└─{'─' * ( title_lspace)}{'─'*len(title)}{'─' * (title_rspace)}─┘")

        stdscr.refresh()
        return True
