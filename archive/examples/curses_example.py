####################################
# pip install windows-curses
####################################

# Slightly modified by nopeless

import curses

stdscr = curses.initscr()

# Util function


def clamp(min_val, val, max_val):
    return max(min_val, min(val, max_val))


def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True:
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Exit menu
        if k == ord("q"):
            return

        # Deal with arrow keys
        if k == curses.KEY_DOWN:
            cursor_y += 1
        elif k == curses.KEY_UP:
            cursor_y -= 1
        elif k == curses.KEY_RIGHT:
            cursor_x += 1
        elif k == curses.KEY_LEFT:
            cursor_x -= 1

        cursor_x = clamp(0, cursor_x, width - 1)
        cursor_y = clamp(0, cursor_y, height - 1)

        # Declaration of strings
        title = "Curses example"[: width - 1]
        subtitle = "Written by Clay McLeod"[: width - 1]
        # Two ways of padding
        keystr = (
            f"{f'Last key pressed: {k}':{width-1}}"
            if k != 0
            else "No key press detected...".ljust(width - 1)
        )
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(
            cursor_x, cursor_y
        )

        # Centering calculations
        # This can be done with f strings as well
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # As you can see here, the format is
        # Turn on, then turn off
        # I will write a light weight framework to modularize this

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(
            height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1)
        )
        stdscr.attroff(curses.color_pair(3))

        # Rendering title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(start_y, start_x_title, title)
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, "-" * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()
