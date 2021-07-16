import asyncio
import curses

from pynput import keyboard

from client.appstate import AppState
from game.engine import Engine
from game.entities.ball import Ball
from game.entities.entity_type import EntityType
from game.entities.player import Player

from ._ui import UI
from .widget.progress_bar import ProgressBar
from .widget.simple_button import Button
from .widget.simple_textbox import Box


def clamp(a, b, c):
    return max(a, min(b, c))


class GamePlay(UI):
    """the main game"""

    def __init__(self):
        super().__init__("menu screen")
        self.time = 0

    async def view(self, app):
        # Required
        super().view(app)

        self.disp_h, self.disp_w = 50, 150
        self.c_y, self.c_x = self.window.getmaxyx()
        self.c_y = int(self.c_y / 2)
        self.c_x = int(self.c_x / 2)

        # self.connecting_to_server = ProgressBar(
        #     width=32, y=self.c_y, x=self.c_x, message_text="Connecting to server"
        # )

        # loading = 0
        # dots = 0
        # while True:
        #     loading = (loading % 100) + 10
        #     dots = (dots % 3) + 1
        #     self.connecting_to_server.message = f"Connecting to server{'.' * dots}"
        #     self.connecting_to_server.set_progress(loading)
        #     self.connecting_to_server.refresh()
        #     curses.doupdate()
        #     await asyncio.sleep(0.2)

        game_engine = Engine(debug=True)
        await game_engine.run()

        _150 = 150
        _300 = 300

        pad = curses.newpad(_150, _300)
        pad.border(0)

        x = 0
        y = 0

        def t(tup):
            """Returns a scaled down version. x,y (600, 600) -> (300, 150)"""
            return (tup[0] / 2, tup[1] / 4)

        def st(tup):
            """
            Returns a scaled down version. y,x (600, 600) -> (150, 300)

            Also ensures that it will be in the valid range
            """
            return (clamp(0, tup[0] / 2, _300), clamp(0, tup[1] / 4, _150))

        # def scyx(x, y):
        #     """Short for screen clamp x. accepts (x,y) returns (y, x)"""
        #     return clamp(0, y, _150), clamp(0, x, _300)

        def scx(x):
            """Short for screen clamp x."""
            return clamp(0, x, _300 - 1)

        def scy(y):
            """Short for screen clamp y."""
            return clamp(0, y, _150 - 1)

        # def is_range_in_col_b(scale, a, p, b):
        #     """Private util function. `-1 <= scale <= 1`, `a <= p <= b`"""

        """palette
        █
         │ ─ ┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘
        ■■
        """
        while True:
            # Redraw the pad
            pad.clear()
            pad.border(0)
            for entity in game_engine.entities.values():
                if entity.type == EntityType.PLAYER:
                    # Render the player
                    p = st(entity.position)
                    # print(p)
                    pad.addstr(int(p[1]), int(p[0]), "⌧")
                    if entity.horizontal:
                        # Hitbox
                        arm_y = int(p[1])
                        arm_left = int(scx(p[0] - 25 / 2))
                        arm_right = int(scx(p[0] + 25 / 2))
                        for i in range(arm_left, arm_right + 1):
                            pad.addch(arm_y, i, "─")

                        # bcb
                        bcb_y = int(p[1])
                        bcb_left = int(scx(p[0] + 21 / 2 * entity.bar_loc - 2))
                        bcb_right = int(scx(p[0] + 21 / 2 * entity.bar_loc + 2))
                        for i in range(bcb_left, bcb_right):
                            pad.addch(bcb_y, i, "■")
                    else:
                        # Hitbox
                        arm_x = int(p[0])
                        arm_top = int(scy(p[1] - 25 / 4))
                        arm_bottom = int(scy(p[1] + 25 / 4))
                        a = 1
                        for i in range(arm_top, arm_bottom):
                            pad.addch(i, arm_x, "│")

                        # bcb
                        bcb_x = int(p[0])
                        bcb_top = int(scy(p[1] + 21 / 4 * entity.bar_loc - 1))
                        bcb_bottom = int(scy(p[1] + 21 / 4 * entity.bar_loc + 1))
                        for i in range(bcb_top, bcb_bottom):
                            pad.addch(i, bcb_x, "█")

                elif entity.type == EntityType.BALL:
                    # Render the player
                    p = st(entity.position)
                    pad.addstr(int(scy(p[1])), int(scx(p[0])), "⊙")
                    # print(p)
            pad.refresh(
                y,
                x,
                0,
                0,
                self.disp_h,
                self.disp_w,
            )

            if app.input_manager.is_pressed("w"):
                y -= 1
            if app.input_manager.is_pressed("s"):
                y += 1
            if app.input_manager.is_pressed("a"):
                x -= 1
            if app.input_manager.is_pressed("d"):
                x += 1

            y = clamp(0, y, pad.getmaxyx()[0] - 51)
            x = clamp(0, x, pad.getmaxyx()[1] - 151)

            # self.window.addstr(0, 0, f"x:{x} y:{y}")

            await asyncio.sleep(0.05)
            # app.screen.clear()
            app.screen.refresh()

        await asyncio.sleep(1000)

        self.time += 10
        my_bar = ProgressBar(width=32, y=1, x=0, message_text="Press space to exit")
        my_bar.set_progress(self.time)
        my_button = Button(2, 34, go_to=AppState.GAME_OVER)
        editor = Box(3, 20, 5, 0)
        # You can manually refresh them as well
        self.widgets = [my_bar, my_button, editor]
        self.input_manager = app.input_manager
        self.register_input_managers(
            *self.widgets
        )  # Give them access to the input_manager
        res = None
        i = 0
        while True:
            # Main loop for rendering the menu
            i += 1
            self.window.addstr(
                0,
                0,
                f"I am a menu {i} - is 'i' pressed? {'yes' if self.input_manager.is_pressed('i') else 'no '}",
            )
            my_bar.set_progress(i % 100)
            if res := self.refresh():
                break
            curses.doupdate()
            await asyncio.sleep(0.1)
        return res


# Return single menu object
game_play = GamePlay()
