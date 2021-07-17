# input manager imports keyboard.py
# TEMPORARY
import curses
from types import SimpleNamespace
from typing import Optional

from pynput import keyboard

from .active_window import is_focused
from .state import InputState


def is_typeable_char(key):
    try:
        key.char
        return True
    except AttributeError:
        return False


def get_char_of_key(key):
    return key.char


class InputManager:
    """
    Acts like the `keyboard` module

    Forwards the api
    """

    def __init__(self, allow_text_mode=True, mock=False):
        """
        Creates an InputManager that emits events

        Initializes a keyboard
        """
        self.text = None
        self.state = InputState.GAMEPAD
        self.last_state = self.state

        self.callback = SimpleNamespace()
        self.callback.on_press = lambda _: None
        self.callback.on_release = lambda _: None
        self.callback.on_text_start = lambda _: None
        self.callback.on_text_update = lambda _: None
        self.callback.on_text_end = lambda _: None

        self.pressed_keys = set()

        on_press = None
        text_manager = None

        if allow_text_mode:
            # Text callback methods are managed here
            # this is the only place where self.text is changed (except for self.set_text)
            def text_manager(k):
                if self.text is None:
                    self.text = []
                if is_typeable_char(k):
                    ch = get_char_of_key(k)
                    if ord(ch) < 32 or 126 < ord(ch) < 128:
                        return
                    self.text.append(ch)
                    self.callback.on_text_update(self.get_text())
                elif k == keyboard.Key.space:
                    self.text.append(" ")
                    self.callback.on_text_update(self.get_text())
                elif k == keyboard.Key.enter:
                    self.callback.on_text_end(self.get_text())
                    self.exit_input()
                elif k == keyboard.Key.backspace:
                    if len(self.text):
                        self.text.pop()
                    else:
                        self.text = None
                    self.callback.on_text_update(self.get_text())

            def on_press(k):
                # FIXME find a way to disable curses input buffer
                curses.flushinp()
                if not is_focused():
                    return

                # Add attribute so its easier to handle from uis

                # Handle
                self.pressed_keys.add(k)
                if self.state == InputState.TYPING:
                    text_manager(k)
                else:
                    k.char = k.char if is_typeable_char(k) else None
                    self.callback.on_press(k)

        else:

            def on_press(k):
                # FIXME find a way to disable curses input buffer
                curses.flushinp()
                if not is_focused():
                    return

                # Add attribute so its easier to handle from uis
                self.char = k.char if is_typeable_char(k) else None

                # Handle
                self.pressed_keys.add(k)
                self.callback.on_press(k)

        def on_release(k):
            if not is_focused():
                return

            # Handle
            self.pressed_keys.discard(k)
            self.callback.on_release(k)

        if not mock:
            keyboard.Listener(on_press=on_press, on_release=on_release).start()

    #############################################
    # Call back methods
    #############################################

    def hook(self, *args):
        """`keyboard.hook` Raw hook"""
        raise NotImplementedError
        # return keyboard.hook(*args)

    def unhook(self, *args):
        """`keyboard.unhook`"""
        raise NotImplementedError
        # return keyboard.unhook(*args)

    def on_press(self, cb):
        self.callback.on_press = cb

    def on_release(self, cb):
        self.callback.on_release = cb

    def on_text_start(self, cb):
        self.callback.on_text_start = cb

    def on_text_update(self, cb):
        self.callback.on_text_update = cb

    def on_text_end(self, cb):
        """Supplies an"""
        self.callback.on_text_end = cb

    ###############################################
    # Normal methods
    ###############################################

    def trigger_input(self):
        self.set_state(InputState.TYPING)

    def is_pressed(self, key):
        if not is_focused():
            return False
        if isinstance(key, str):
            key = keyboard.KeyCode.from_char(key)
        if self.state == InputState.TYPING:
            return False
        return key in self.pressed_keys

    def exit_input(self):
        """Exits input mode to original mode"""
        # this shouldn't happen
        if self.last_state == InputState.TYPING:
            self.state = InputState.GAMEPAD
            return
        self.last_state, self.state = self.state, self.last_state

    def set_state(self, state: InputState) -> None:
        """Has to be one of the states"""
        if self.state == state:
            return
        self.last_state = self.state
        self.state = state
        if state == InputState.TYPING:
            self.on_text_start(self.get_text())

    def get_text(self) -> Optional[str]:
        if self.text is not None:
            return "".join(self.text)
        return None

    def set_text(self, s: str):
        self.text = list(s)


input_manager = InputManager()
