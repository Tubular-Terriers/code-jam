import curses
import sys
from enum import Enum, auto
from types import SimpleNamespace

from pynput import keyboard

from ._widget import Widget


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
        progress_color_pair_id: int = None,
        progress_left_color_pair_id: int = None,
        selected=False,
        toggled=False,
        require_active=True,
        go_to=None,
        callback=None,
        progress: int = 0,
        orientation: Orientation = Orientation.HORIZONTAL,
    ):
        super().__init__("slider")
        self.require_selected = require_active
        self.x = x
        self.y = y
        self.text = text
        self.text_color_pair_id = text_color_pair_id
        self.frame_color_pair_id = frame_color_pair_id
        self.height = height if height >= 6 else 6
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
        self.progress = progress / 100
        self.orientation: Orientation = orientation
        self.max_progress: int = 1
        self.min_progress: int = 0
        self.progress_color_pair_id: int = progress_color_pair_id
        self.progress_left_color_pair_id: int = progress_left_color_pair_id

    def refresh(self):
        # TEXT
        if self.selected and self.text is not None:

            if self.text_color_pair_id is not None:
                self.window.attron(curses.color_pair(self.text_color_pair_id))

            self.window.addstr(0, self.width // 2 - (len(self.text) // 2), self.text)

            if self.text_color_pair_id is not None:
                self.window.attroff(curses.color_pair(self.text_color_pair_id))

        # FRAME
        if self.selected and self.frame_color_pair_id is not None:
            self.window.attron(curses.color_pair(self.frame_color_pair_id))

        self.window.addstr(1, 0, self.upper_left_corner)

        # HORIZONTAL ORIENTATION
        if self.orientation is Orientation.HORIZONTAL:
            for x in range(1, self.width - 2):
                self.window.addstr(1, x, self.horizontal_border)

            self.window.addstr(1, self.width - 2, self.upper_right_corner)

            for y in range(2, self.height - 3):
                self.window.addstr(y, 0, self.vertical_border)

                if self.frame_color_pair_id is not None:
                    self.window.attroff(curses.color_pair(self.frame_color_pair_id))

                if self.progress_color_pair_id is not None:
                    self.window.attron(curses.color_pair(self.progress_color_pair_id))

                completed = int(self.progress * (self.width - 2))

                for x in range(1, completed):
                    self.window.addstr(y, x, self.complete_progress)

                if self.progress_color_pair_id is not None:
                    self.window.attroff(curses.color_pair(self.progress_color_pair_id))

        # VERTICAL ORIENTATION
        elif self.orientation is Orientation.VERTICAL:
            pass

        self.window.noutrefresh()

    def update_progress(self, key, increment):
        value = increment / 100

        if key == keyboard.Key.right:
            self.progress += (
                value if self.progress <= self.max_progress else self.max_progress
            )
        elif key == keyboard.Key.left:
            self.progress -= (
                value if self.progress >= self.min_progress else self.min_progress
            )

        self.refresh()

    def select(self):
        self.selected = True
        self.refresh()

    def unselect(self):
        self.selected = False
        self.refresh()
