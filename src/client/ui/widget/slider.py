import curses
import sys

from pynput import keyboard
from types import SimpleNamespace

from ._widget import Widget
from enum import Enum, auto


class Orientation(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class Slider(Widget):
    def __init__(
        self,
        y,
        x,
        key=None,
        height=4,
        width=11,
        text=None,
        frame_color_pair_id: int = None,
        text_color_pair_id: int = None,
        selected=False,
        toggled=False,
        require_active=True,
        go_to=None,
        callback=None,
        progress: int = 0,
    ):
        super().__init__("slider")
        self.require_selected = require_active
        self.x = x
        self.y = y
        self.text = text
        self.text_color_pair_id = text_color_pair_id
        self.frame_color_pair_id = frame_color_pair_id
        self.height = height if height >= 4 else 4
        self.width = width if width >= 10 else 10
        self.window = curses.newwin(self.height, self.width, y, x)
        self.toggled = toggled
        self.callback = callback
        self.selected = selected
        self.toggle_count = 0
        self.key = key
        self.go_to = go_to
        self.horizontal_border = "─"
        self.vertical_border = "│"
        self.upper_left_corner = "┌"
        self.upper_right_corner = "┐"
        self.bottom_left_corner = "└"
        self.bottom_right_corner = "┘"
        self.complete_progress = "#"
        self.progress_left = "-"
        self.progress = progress // 100
        self.orientation: Orientation = Orientation.HORIZONTAL
        self.max_progress: int = 1
        self.min_progress: int = 0

    def refresh(self):
        if self.selected and self.text is not None:
            self.window.addstr(0, self.width // 2 - (len(self.text) // 2), self.text)

        if self.selected and self.frame_color_pair_id is not None:
            self.window.attron(curses.color_pair(self.frame_color_pair_id))

        self.window.addstr(1, 0, self.upper_left_corner)

        self.window.addstr(1, 1, self.horizontal_border * (self.width - 2))
        self.window.addstr(1, self.width - 1, self.upper_right_corner)
        for y in range(1, self.height - 2):
            self.window.addstr(y, 0, self.vertical_border)
        self.window.addstr(self.height - 2, 0, self.bottom_left_corner)
        for y in range(1, self.height - 2):
            self.window.addstr(y, self.width - 1, self.vertical_border)
        self.window.addstr(
            self.height - 2, 1, self.horizontal_border * (self.width - 2)
        )
        self.window.addstr(self.height - 2, self.width - 1, self.bottom_right_corner)

        self.window.noutrefresh()
        if self.toggle_count >= 1 and (
            self.selected is True or self.require_selected is False
        ):
            if self.go_to is not None:
                return self.go_to

    def update_progress(self, key, increment):
        value = increment // 100

        if key == keyboard.Key.right:
            self.progress += (
                value if self.progress <= self.max_progress else self.max_progress
            )
        elif key == keyboard.Key.left:
            self.progress -= (
                value if self.progress >= self.min_progress else self.min_progress
            )

    def select(self):
        self.selected = True
        self.refresh()

    def toggle(self):
        self.toggle_count += 1
        self.toggled = not self.toggled
        self.refresh()

    def press_on(self, key):
        if key == self.key or key.char == self.key:
            self.toggle_count += 1
            self.toggled = not self.toggled
            if self.callback is not None:
                self.callback()
            self.refresh()
        else:
            return key
