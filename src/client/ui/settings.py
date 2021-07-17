import asyncio
import curses
import random
from pynput import keyboard
from client.appstate import AppState
from ._ui import UI
from .widget.button import Button
from .widget.progress_bar import ProgressBar
from .widget.slider import Slider


class Settings(UI):
    def __init__(self):
        super().__init__("settings_screen")
        self.title = [
            r"  ____       _   _   _                 ",
            r" / ___|  ___| |_| |_(_)_ __   __ _ ___ ",
            r" \___ \ / _ \ __| __| | '_ \ / _` / __|",
            r"  ___) |  __/ |_| |_| | | | | (_| \__ \\",
            r" |____/ \___|\__|\__|_|_| |_|\__, |___/",
            r"                             |___/     "
        ]
        self.height = 0
        self.width = 0
        self.selected_widget = 0
        self.increment = 10
        self.increment_slider = None

    async def view(self, app):
        super().view(app)
        self.height, self.width = self.window.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, 215, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.window.attron(curses.color_pair(2))

        y = 0
        for text in self.title:
            self.window.addstr(
                self.height // 5 - len(self.title) + y,
                self.width // 2 - len(text) // 2,
                text,
                curses.color_pair(2),
            )
            y += 1

        self.window.attroff(curses.color_pair(2))
        self.window.attron(curses.A_NORMAL)

        width = 25
        menu_button = Button(
            self.height - self.height // 5,
            self.width // 2 - (width // 2),
            text_color_pair_id=4,
            frame_color_pair_id=5,
            width=width,
            text="Back",
            key=keyboard.Key.enter,
            go_to=AppState.MAIN_MENU,
            selected=self.selected_widget == 0
        )
        
        width = 4
        height = 20
        self.increment_slider = Slider(
            self.height // 2 - (height // 2),
            self.width - width - 15,
            text="UP/DOWN",
            frame_color_pair_id=5,
            height=height,
            width=width,
            selected=self.selected_widget == 1
        )
        
        self.window.addstr(self.height // 2 + (height // 2),
                           self.width - width - 16,
                           "Set increment")

        width = 55
        sfx_volume_slider = Slider(self.height // 2 - (height // 2),
                                   self.width // 2 - (width // 2),
                                   text_color_pair_id=4,
                                   frame_color_pair_id=5,
                                   width=width,
                                   selected=self.selected_widget == 2
                                   )

        self.widgets = [menu_button, self.increment_slider, sfx_volume_slider]
        self.refresh()

        while True:
            if res := self.refresh():
                break
            self.update()
            curses.doupdate()
            await asyncio.sleep(.1)
        return res
    
    def update(self):
        self.increment = self.increment_slider.progress

    def press_on(self, key):
        if self.widgets[self.selected_widget] == self.increment_slider:
            if key == keyboard.Key.up:
                self.increment_slider.update_progress(key, 1)
            elif key == keyboard.Key.down:
                self.increment_slider.update_progress(key, 1)
            elif key == keyboard.Key.right:
                self.selected_widget = 0
            elif key == keyboard.Key.left:
                self.selected_widget = 0
        else:
            if key == keyboard.Key.up:
                self.widgets[self.selected_widget].selected = False
                if not self.selected_widget == 0:
                    self.selected_widget -= 1
                else:
                    self.selected_widget = len(self.widgets) - 1
    
                self.widgets[self.selected_widget].selected = True
    
            elif key == keyboard.Key.down:
                self.widgets[self.selected_widget].selected = False
    
                if not self.selected_widget == len(self.widgets) - 1:
                    self.selected_widget += 1
                else:
                    self.selected_widget = 0
    
                self.widgets[self.selected_widget].selected = True

            elif key == keyboard.Key.right:
                if not self.selected_widget == 0:
                    self.widgets[self.selected_widget].update_progress(key, self.increment)
                    
            elif key == keyboard.Key.left:
                if not self.selected_widget == 0:
                    self.widgets[self.selected_widget].update_progress(key, self.increment)
    
            elif key == keyboard.Key.enter:
                if self.selected_widget == 0:
                    self.widgets[self.selected_widget].toggle()
                    
            elif key == keyboard.Key.esc:
                self.widgets[self.selected_widget].selected = False
                self.selected_widget = 0


settings = Settings()
