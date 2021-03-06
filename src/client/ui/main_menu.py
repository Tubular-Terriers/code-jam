import asyncio
import curses
import random
import sys

from pynput import keyboard

from client.appstate import AppState
from client.input.active_window import is_focused
from client.settings.config import Config
from client.settings.settings import Settings
from client.sound.sound_effects_engine import SoundEffectsEngine
from client.sound.sounds import SoundEffects

from ._ui import UI
from .widget.button import Button


class Main_menu(UI):
    """makes main screen ui"""

    def __init__(self):
        super().__init__("main_menu_scr")
        self.message = [
            r" _   _                        _             ",
            r"| | | |                      (_)            ",
            r"| |_| |__   ___   ____   ___  _ ____   ____ ",
            r"| __|  _ \ / _ \ |  _ \ / _ \| |  _ \ / _  |",
            r"| |_| | | |  __/ | |_) | (_) | | | | | (_| |",
            r" \__|_| |_|\___| |  __/ \___/|_|_| |_|\__, |",
            r"                 | |                   __/ |",
            r"                 |_|                  |___/ ",
        ]
        self.horizontal_border = "─"
        self.vertical_border = "│"
        self.upper_right_corner = "┐"
        self.upper_left_corner = "┌"
        self.bottom_left_corner = "└"
        self.bottom_right_corner = "┘"
        self.ball = "●"
        self.ball_pos_x = None
        self.ball_pos_y = None
        self.ball_speed_y = random.choice([num for num in range(-1, 1) if num != 0])
        self.ball_speed_x = random.choice([num for num in range(-1, 1) if num != 0])
        self.board_start_y = None
        self.board_end_y = None
        self.board_start_x = 10
        self.board_end_x = None
        self.button_spacing = None
        self.colors_range = range(1, 9)
        self.selected_color = 1
        self.selected_widget = 0
        self.config = Config()
        self.sound_engine = SoundEffectsEngine(
            int(self.config.get(Settings.SFX_VOLUME))
        )

    async def move_ball(self):
        # TODO: Fix corners

        self.window.addstr(self.ball_pos_y, self.ball_pos_x, " ")

        self.ball_pos_y += self.ball_speed_y
        self.ball_pos_x += self.ball_speed_x

        if self.ball_pos_y >= self.board_end_y:
            self.ball_pos_y = self.board_end_y - 1
            self.ball_speed_y = -self.ball_speed_y

            if is_focused() or not bool(
                self.config.get(Settings.MUTE_GAME_ON_FOCUS_LOSS)
            ):
                self.sound_engine.play_sound(SoundEffects.WALL_BOUNCE)

            self.window.addstr(self.board_end_y, self.ball_pos_x, " ")

            if self.ball_pos_x == self.board_end_x - 1:
                self.window.addstr(
                    self.board_end_y, self.board_end_x, self.bottom_right_corner
                )
            else:
                self.window.addstr(
                    self.board_end_y, self.ball_pos_x, self.horizontal_border
                )

            self.switch_ball_color()

        if self.ball_pos_y <= self.board_start_y:

            self.ball_pos_y = self.board_start_y + 1
            self.ball_speed_y = -self.ball_speed_y

            if is_focused() or not bool(
                self.config.get(Settings.MUTE_GAME_ON_FOCUS_LOSS)
            ):
                self.sound_engine.play_sound(SoundEffects.WALL_BOUNCE)

            self.window.addstr(self.board_start_y, self.ball_pos_x, " ")

            self.window.addstr(
                self.board_start_y, self.ball_pos_x, self.horizontal_border
            )

            self.switch_ball_color()

        if self.ball_pos_x >= self.board_end_x:
            self.ball_pos_x = self.board_end_x - 1
            self.ball_speed_x = -self.ball_speed_x

            if is_focused() or not bool(
                self.config.get(Settings.MUTE_GAME_ON_FOCUS_LOSS)
            ):
                self.sound_engine.play_sound(SoundEffects.WALL_BOUNCE)

            self.window.addstr(self.ball_pos_y, self.board_end_x, " ")
            self.window.addstr(self.ball_pos_y, self.board_end_x, self.vertical_border)

            self.switch_ball_color()

        if self.ball_pos_x <= self.board_start_x:
            self.ball_pos_x = self.board_start_x + 1
            self.ball_speed_x = -self.ball_speed_x

            if is_focused() or not bool(
                self.config.get(Settings.MUTE_GAME_ON_FOCUS_LOSS)
            ):
                self.sound_engine.play_sound(SoundEffects.WALL_BOUNCE)

            self.window.addstr(self.ball_pos_y, self.board_start_x, " ")
            self.window.addstr(
                self.ball_pos_y, self.board_start_x, self.vertical_border
            )

            self.switch_ball_color()

        self.window.attron(curses.A_BOLD)
        self.window.addstr(self.ball_pos_y, self.ball_pos_x, self.ball)

    def switch_ball_color(self):
        available_colors = [
            color_id
            for color_id in self.colors_range
            if color_id != self.selected_color
        ]
        self.selected_color = random.choice(available_colors)
        self.window.attron(curses.color_pair(self.selected_color))

    async def view(self, app):
        super().view(app)
        height, width = self.window.getmaxyx()
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
        for text in self.message:
            self.window.addstr(
                height // 2 - len(self.message) + y,
                width // 2 - len(text) // 2,
                text,
                curses.color_pair(2),
            )
            y += 1

        self.window.attroff(curses.color_pair(2))
        self.window.attron(curses.A_NORMAL)
        self.refresh()

        self.board_end_x = width - self.board_start_x

        self.board_start_y = height // 10
        self.board_end_y = height - 15

        for x in range(self.board_start_x, self.board_end_x):
            self.window.addstr(
                self.board_start_y, x, self.horizontal_border, curses.color_pair(1)
            )

        for y in range(self.board_start_y + 1, self.board_end_y):
            self.window.addstr(y, self.board_start_x, self.vertical_border)

        self.window.addstr(
            self.board_start_y, self.board_start_x, self.upper_left_corner
        )
        self.window.addstr(
            self.board_start_y, self.board_end_x, self.upper_right_corner
        )

        for y in range(self.board_start_y + 1, self.board_end_y):
            self.window.addstr(y, self.board_end_x, self.vertical_border)

        self.window.addstr(
            self.board_end_y, self.board_start_x, self.bottom_left_corner
        )
        self.window.addstr(self.board_end_y, self.board_end_x, self.bottom_right_corner)

        for x in range(self.board_start_x + 1, self.board_end_x):
            self.window.addstr(self.board_end_y, x, self.horizontal_border)

        self.ball_pos_y = (
            self.board_end_y - self.board_start_y
        ) // 2 + self.board_start_y
        self.ball_pos_x = (
            self.board_end_x - self.board_start_x
        ) // 2 + self.board_start_x

        self.window.attron(curses.A_BOLD)
        self.window.attron(curses.color_pair(3))

        self.window.addstr(self.ball_pos_y, self.ball_pos_x, self.ball)

        self.window.attroff(curses.color_pair(3))
        self.window.attroff(curses.A_BOLD)

        host_game_button = Button(
            self.board_end_y + 5,
            self.board_end_x // 6,
            text="Host a game",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            width=17,
            key=keyboard.Key.enter,
            go_to=AppState.HOST_GAME,
            selected=self.selected_widget == 0,
        )

        join_game_button = Button(
            self.board_end_y + 5,
            (self.board_end_x // 6) * 2,
            text="Join a game",
            text_color_pair_id=7,
            frame_color_pair_id=5,
            width=17,
            key=keyboard.Key.enter,
            go_to=AppState.JOIN_GAME,
            selected=self.selected_widget == 1,
        )

        settings_button = Button(
            self.board_end_y + 5,
            (self.board_end_x // 6) * 3,
            width=18,
            text="Settings",
            text_color_pair_id=1,
            frame_color_pair_id=5,
            key=keyboard.Key.enter,
            go_to=AppState.SETTINGS_SCR,
            selected=self.selected_widget == 2,
        )

        credits_button = Button(
            self.board_end_y + 5,
            (self.board_end_x // 6) * 4,
            width=17,
            text="Credits",
            text_color_pair_id=1,
            frame_color_pair_id=5,
            key=keyboard.Key.enter,
            go_to=AppState.CREDITS_SCR,
            selected=self.selected_widget == 3,
        )

        exit_button = Button(
            self.board_end_y + 5,
            (self.board_end_x // 6) * 5,
            text="Exit",
            text_color_pair_id=6,
            frame_color_pair_id=5,
            width=18,
            key=keyboard.Key.enter,
            go_to=AppState.EXIT,
            selected=self.selected_widget == 4,
        )
        self.widgets = [
            host_game_button,
            join_game_button,
            settings_button,
            credits_button,
            exit_button,
        ]
        self.refresh()

        while True:
            if res := self.refresh():
                break
            await self.move_ball()
            curses.doupdate()
            await asyncio.sleep(0.08)
        return res

    def press_on(self, key):
        if key == keyboard.Key.left:
            self.widgets[self.selected_widget].selected = False
            if not self.selected_widget == 0:
                self.selected_widget -= 1
            else:
                self.selected_widget = len(self.widgets) - 1
            self.widgets[self.selected_widget].selected = True

        elif key == keyboard.Key.right:
            self.widgets[self.selected_widget].selected = False
            if not self.selected_widget == len(self.widgets) - 1:
                self.selected_widget += 1
            else:
                self.selected_widget = 0

            self.widgets[self.selected_widget].selected = True

        elif key == keyboard.Key.enter:
            self.widgets[self.selected_widget].toggle()


main_menu = Main_menu()
