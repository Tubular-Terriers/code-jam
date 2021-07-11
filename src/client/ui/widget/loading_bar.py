import curses
import time

curses.initscr()

class loading_bar:
    def __init__(self, width, y, x, message = None):
        self.height = 3
        self.width = width
        self.y = y
        self.x = x
        self.message = message
        self.win = curses.newwin(self.height, self.width, self.y, self.x)
        self.win.border(0)

    def update(self):
        if self.message !=None:
            self.win.addstr(1,1,self.message)
        x = int(self.progress)
        x = x*((self.width-2) / float(100))
        x = int(x)
        display = '#'
        if x != 0:
            self.win.addstr(1, x, f"{display}")
            self.win.refresh()

    def set_progress(self, progress: float):
        self.progress= progress
        self.update()

a=loading_bar(width=32, y=0, x=0)
loading = 0
while loading < 100:
    loading += 1
    time.sleep(0.03)
    a.set_progress(loading)
