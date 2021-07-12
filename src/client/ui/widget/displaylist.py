import curses
import time  # only for debugging

stdscr = curses.initscr()


class Listdisplay:
    def __init__(self, lst, start_x, start_y, height, width, headers=None) -> None:
        """Lst is 2-d. i th list in lst is content of i+1 tab

        Each string in lst should not be of more length than width
        scroling is available only in vertical direction
        """
        self.start_x = start_x
        self.start_y = start_y
        self.height = height
        self.width = width
        self.currentpos = 0
        self.currenttab = 0
        self.lst = lst

        curses.curs_set(0)
        newwin = curses.newwin(height, width, start_y, start_x)
        newwin.border(0)
        newwin.refresh()
        self.display()

    def display(self, tab=0):
        self.pad = curses.newpad(1 + len(self.lst[tab]) + 1, self.width)
        for n in range(len(self.lst[tab])):
            self.pad.addstr(n, 1, self.lst[tab][n])

        self.refresh_pad()

    def scrollup(self):
        self.currentpos += 1
        self.currentpos = min(
            len(self.lst[self.currenttab]) - self.height + 3, self.currentpos
        )
        self.refresh_pad()

    def scrolldown(self):
        self.currentpos -= 1
        self.currentpos = max(0, self.currentpos)
        self.refresh_pad()

    def switchtab_right(self):
        self.currentpos = 0
        self.currenttab += 1
        self.currenttab = min(len(self.lst), self.currenttab)
        self.pad.erase()
        self.refresh_pad()
        self.display(self.currenttab)

    def switchtab_left(self):
        self.currentpos = 0
        self.currenttab -= 1
        self.currenttab = max(0, self.currenttab)
        self.pad.erase()
        self.refresh_pad()
        self.display(self.currenttab)

    def refresh_pad(self):
        self.pad.refresh(
            self.currentpos,
            0,
            self.start_y + 1,
            self.start_x + 1,
            self.height - 1,
            self.width - 1,
        )


def main(stdscr):
    curses.init_color(1, 0, 0, 0)
    lst = [
        ["hii", "hello", "dkfjalkfjkjlkjlkj", "lajdflkdf"],
        ["tab2", "tambs"],
    ]  # for debugging
    stdscr.clear()
    a = Listdisplay(lst, 1, 1, 5, 10)
    time.sleep(2)
    a.scrollup()
    time.sleep(2)
    a.scrollup()
    time.sleep(2)
    a.scrolldown()
    time.sleep(2)
    a.switchtab_right()
    time.sleep(2)
    a.switchtab_left()
    time.sleep(2)


if __name__ == "__main__":
    curses.wrapper(main)
