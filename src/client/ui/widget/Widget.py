# The base class for all widgets


class Widget:
    def __init__(self, name):
        self.name = name
        pass

    def press_on(self, key):
        """Called with the argument `key`"""
        pass

    def refresh(self, key):
        if self.window:
            self.window.erase()
            self.window.refresh()
