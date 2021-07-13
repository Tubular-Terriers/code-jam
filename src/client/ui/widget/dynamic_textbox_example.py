#!/usr/bin/env python

import curses
import curses.textpad
import asyncio
import pygame
from pynput import keyboard


def static_vars(**kwargs):
    def async_wrapper(callback):
        def inner(key):
            temp = asyncio.run(callback(key))
            # key combinations traitement
            if temp == -1:
                kwargs["_str"] = kwargs["_str"][:-1]
            else:
                kwargs["_str"] += temp
            print_scr(window, kwargs["_str"])

        return inner

    return async_wrapper


@static_vars(_str="")
async def on_release(key):
    # await asyncio.sleep(1)  # async support
    if key == keyboard.Key.esc:
        # Stop listener
        global crashed
        crashed = True
        return False
    if key == keyboard.Key.backspace:
        return -1
    try:
        return key.char
    except AttributeError:
        return ""


def print_scr(stdscr, text):
    stdscr.clear()
    print(text)
    title = "Text Box"
    width = max(len(title), len(text))
    title_lspace = (width - len(title)) // 2
    title_rspace = width - len(title) - title_lspace
    stdscr.addstr(0, 0, f"┌─{'─' * (title_lspace)}{title}{'─' * (title_rspace)}─┐")
    text_lspace = (width - len(text)) // 2
    text_rspace = width - len(text) - text_lspace
    stdscr.addstr(1, 0, f"│ {' ' * ( text_lspace)}{text}{' ' * ( text_rspace)} │")
    stdscr.addstr(
        2, 0, f"└─{'─' * ( title_lspace)}{'─'*len(title)}{'─' * (title_rspace)}─┘"
    )

    stdscr.refresh()
    return True


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

window = curses.newwin(20, 20, 0, 0)


# non-blocking listener
listener = keyboard.Listener(on_release=on_release)
listener.start()

# for non-blocking code, used below loop
pygame.init()

clock = pygame.time.Clock()
crashed = False
counter = 1
while not crashed:
    counter += 1
    clock.tick(1)  # will be 10 in the next run

# classic conf
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
