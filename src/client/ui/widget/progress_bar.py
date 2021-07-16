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


class MessageAlignment(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


class MessageCreationFailed(Exception):
    pass


class ProgressBar(Widget):
    '''a simple widget for adding a progress bar'''
    def __init__(
        self,
        width: int,
        x: int,
        y: int,
        height: int = 1,
        message_text: str = None,
        message_alignment: MessageAlignment = MessageAlignment.CENTER,
    ):
        super().__init__("progress bar")
        self.height = height if height >= 4 else 4
        self.width = width if width >= 11 else 11
        self.x = x
        self.y = y
        self.message_text = message_text
        self.message_alignment = message_alignment
        self.message = None if message_text is None else self._create_message_()
        # print(self.message)
        self.window = curses.newwin(self.height, self.width + 3, self.y, self.x)
        self.progress = 0

    def refresh(self):
        # self.window.erase()
        completed = int(self.progress * self.width)

        display = "\n┌" + "─" * self.width + "┐\n"

        rows = self.height - 3
        for row in range(rows):
            display += "│" + "#" * completed + "-" * (self.width - completed) + "│\n"

        display += "└" + "─" * self.width + "┘"

        if self.message is not None:
            display = self.message + display
        try:
            self.window.addstr(0, 1, f"{display}")
        except Exception:
            self.window.addstr(0, 1, f"{display[:self.width]}")
        self.window.noutrefresh()

    def set_progress(self, progress: float):
        """0 to 100"""
        self.progress = progress / 100

    def _create_message_(self) -> str:
        if self.message_alignment is MessageAlignment.CENTER:
            offset = int((self.width - len(self.message_text)) / 2)

            return " " * offset + self.message_text + "" * offset

        elif self.message_alignment is MessageAlignment.LEFT:
            return self.message_text

        elif self.message_alignment is MessageAlignment.RIGHT:
            offset = int(self.width - len(self.message_text))

            return " " * offset + self.message_text
        else:
            raise MessageCreationFailed(
                f"Message alignment must be of type {MessageAlignment}"
            )


if __name__ == "__main__":
    curses.initscr()
    a = ProgressBar(
        height=1,
        width=5,
        y=0,
        x=0,
        message_text="Hello world!",
        message_alignment=MessageAlignment.CENTER,
    )
    loading = 0
    while loading < 100:
        loading += 1
        time.sleep(0.1)
        a.set_progress(loading)
        a.refresh()
        curses.doupdate()

        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("c"):
            raise KeyboardInterrupt
