import asyncio
import curses
import sys

import pygame
import pymunk
from pymunk.vec2d import Vec2d

# FIXME: remove this import
sys.path.append("..")
# from entity_manager import EntityManager
# from engine import Game
# from map.map_manager import MapManager

# flake8: noqa


class RenderEngine:
    """
    Creates instance of renderer

    Parameters:
        space (pymunk.Space): the space to render
    """

    def __init__(self, window, space, width, height, quiet=False):
        # TODO allow this 600 to be a variable
        self.w = width
        self.h = height
        self.space = space
        self.coroutine = None
        self.entities = {}
        self.window = window
        self.magnitude = 2
        self.ball_prev_pos = None
        self.init = False
        # self.loop = asyncio.get_event_loop()
        # if not quiet:
        #    self.init_pygame()

    def static_render(self):
        # print("static render")
        for uuid in self.entities:
            entity = self.entities[uuid]
            type = entity["type"]
            if type == "o":
                global text
                text = "━"
            elif type == "b":
                text = "◉"
            else:
                text = "d"
            self.print_scr(
                entity["x"] * self.magnitude,
                entity["y"] * self.magnitude,
                entity["w"] * self.magnitude,
                text,
            )
            self.init = True
        self.window.refresh()
        return True

    def dynamic_render(self):
        for uuid in self.entities:
            # print("dynamic render")
            entity = self.entities[uuid]
            type = entity["type"]
            if type == "b":
                if pos := self.ball_prev_pos:
                    self.window.delch(pos[1], pos[0])
                self.ball_prev_pos = (
                    entity["x"] * self.magnitude,
                    entity["y"] * self.magnitude,
                )
                print(entity)
                self.print_scr(
                    entity["x"] * self.magnitude,
                    entity["y"] * self.magnitude,
                    entity["w"] * self.magnitude,
                    "◉",
                )
        self.window.refresh()
        return True

    def print_scr(self, x, y, w, text):
        w = int(w)
        x = int(x)
        y = int(y)
        print(x, y, w)
        for i in range(w):
            self.window.addch(y * self.magnitude, (x + i) * self.magnitude, text)
            # self.window.refresh()
        return True


def test():
    stdscr = curses.initscr()
    print(f"max size (y, x): {stdscr.getmaxyx()}")
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    field = curses.newwin(10, 40, 0, 0)
    space = pymunk.Space()
    space.gravity = 0, 0
    mapmng = MapManager()
    print(
        mapmng.set_level(
            0,
            """ --------------------
                -----oooo-oo-oooo---
                --ppp-----o--oo--o--
                ------b-------------
                --o---o-----o-----oo""",
        )
    )
    mapmng.parse(0)
    level_size = mapmng.get_level_size(0)
    renderer = RenderEngine(field, space, level_size[0], level_size[1], True)
    enmng = EntityManager(mapmng.get_raw_interval(0), renderer)
    enmng.parse()
    renderer.print_scr()
    # level_size = mapmng.get_level_size(0)
    # game = Game(level_size[0], level_size[1], renderer, enmng.get_entities(), space)
    # game.generate_borders()
    # game.parse_entities()
    # game.apply_objects()
    # game.start()

    field.getch()

    # classic conf
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    # pygame.quit()


# test()
