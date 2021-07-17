import curses
import sys

from pynput import keyboard

from ._widget import Widget


class Button(Widget):
    def __init__(
        self,
        y,
        x,
        key,
        height=4,
        width=0,
        text=None,
        frame_color_pair_id: int = None,
        text_color_pair_id: int = None,
        selected=False,
        toggled=False,
        require_active=True,
        go_to=None,
        callback=None,
    ):
        super().__init__("button")
        self.require_selected = require_active
        self.x = x
        self.y = y
        self.text = text
        self.text_color_pair_id = text_color_pair_id
        self.frame_color_pair_id = frame_color_pair_id
        self.height = height if height >= 4 else 4
        self.width = width if width > 0 else len(self.text) + 2
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

    def refresh(self):
        if self.selected and self.frame_color_pair_id is not None:
            self.window.attron(curses.color_pair(self.frame_color_pair_id))

        self.window.addstr(0, 0, self.upper_left_corner)
        self.window.addstr(0, 1, self.horizontal_border * (self.width - 2))
        self.window.addstr(0, self.width - 1, self.upper_right_corner)
        for y in range(1, self.height - 2):
            self.window.addstr(y, 0, self.vertical_border)
        self.window.addstr(self.height - 2, 0, self.bottom_left_corner)
        for y in range(1, self.height - 2):
            self.window.addstr(y, self.width - 1, self.vertical_border)
        self.window.addstr(
            self.height - 2, 1, self.horizontal_border * (self.width - 2)
        )
        self.window.addstr(self.height - 2, self.width - 1, self.bottom_right_corner)

        if self.text is not None:
            if self.text_color_pair_id is not None and self.selected:
                self.window.attron(curses.color_pair(self.text_color_pair_id))
            self.window.addstr(
                (self.height - 1) // 2, (self.width - len(self.text)) // 2, self.text
            )
            if self.text_color_pair_id is not None:
                self.window.attroff(curses.color_pair(self.text_color_pair_id))

        self.window.noutrefresh()
        if self.toggle_count >= 1 and (
            self.selected is True or self.require_selected is False
        ):
            if self.go_to is not None:
                return self.go_to

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
