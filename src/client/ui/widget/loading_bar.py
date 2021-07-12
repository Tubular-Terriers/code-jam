import curses
import time

curses.initscr()


class loading_bar:
    def __init__(self, width, y, x, message="lol"):
        self.height = 5
        self.width = width
        self.y = y
        self.x = x
        self.message = message
        self.win = curses.newwin(self.height, self.width, self.y, self.x)

    def update(self):
        self.win.erase() 
        x = int(self.progress)
        x = x/10
        x = int(x)
        display =self.message+"\n┌──────────┐\n│"+"#"*x+"-"*(10-x)+"│\n└──────────┘"
        if x != 0:
            self.win.addstr(0, 1, f"{display}")
            self.win.refresh()

    def set_progress(self, progress: float):
        self.progress = progress
        self.update()

a = loading_bar( 32, 3, 30, "nani") 
loading = 0
while loading < 100:
    loading += 1
    a.set_progress(loading)
    time.sleep(0.03)