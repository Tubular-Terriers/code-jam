# input manager imports keyboard.py
from typing import Optional

import keyboard

from .active_window import is_focused
from .state import InputState


class InputManager:
    """
    Acts like the `keyboard` module

    Forwards the api
    """

    def __init__(self):
        """
        Creates an InputManager that emits events

        Initializes a keyboard
        """
        self.text = None
        self.state = InputState.GAMEPAD

    def is_pressed(self, key):
        if not is_focused():
            return False
        if self.state == InputState.TYPING:
            return False
        return keyboard.is_pressed(key)

    def hook(self, *args):
        """`keyboard.hook` Raw hook"""
        raise NotImplementedError
        # return keyboard.hook(*args)

    def unhook(self, *args):
        """`keyboard.unhook`"""
        raise NotImplementedError
        # return keyboard.unhook(*args)

    def set_state(self, state: InputState) -> None:
        """Has to be one of the states"""
        self.state = state

    def get_text(self) -> Optional[str]:
        if self.text:
            return self.text
        return None

    def hook(self, *args):
        """`keyboard.hook`"""
        return keyboard.hook(*args)

    def unhook(self, *args):
        """`keyboard.unhook`"""
        return keyboard.unhook(*args)

    def on_press(self, cb):
        return keyboard.on_press(cb)


input_manager = InputManager()
