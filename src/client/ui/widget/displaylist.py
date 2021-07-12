import curses
import time  # only for debugging

stdscr = curses.initscr()


class Listdisplay:
    def __init__(self, lst, start_x, start_y, height, width) -> None:

        self.start_x = start_x
        self.start_y = start_y
        self.height = height
        self.width = width
        self.currentpos = 0
        self.lst = lst
        self.pad = curses.newpad(1 + len(lst) + 1, width)

        for n in range(len(lst)):
            self.pad.addstr(n+1, 1, lst[n])
        self.pad.border(0)
        self.pad.refresh(self.currentpos, 0, start_x, start_y, height, width)

    def scrollup(self):
        self.currentpos += 1
        self.currentpos = min(len(self.lst)-self.height+1, self.currentpos)
        self.pad.refresh(self.currentpos, 0, self.start_x, self.start_y, self.height, self.width)

    def scrolldown(self):
        self.currentpos -= 1
        self.currentpos = max(0, self.currentpos)
        self.pad.refresh(self.currentpos, 0, self.start_x, self.start_y, self.height, self.width)

    def switchtab(self, diff):
        pass


def main(stdscr):
    lst = ['hii', 'hello', 'dkfjalkf', 'lajdflkdf']    # for debugging
    stdscr.clear()
    a = Listdisplay(lst, 0, 0, 3, 10)
    time.sleep(2)
    a.scrollup()
    time.sleep(2)
    a.scrolldown()
    time.sleep(2)


if __name__ == "__main__":
    curses.wrapper(main)
