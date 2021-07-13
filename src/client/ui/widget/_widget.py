# The base class for all widgets


class Widget:
    def __init__(self, name):
        self.name = name
        pass

    def press_on(self, key):
        """Called with the argument `key`"""
        pass

    def release_on(self, k):
        pass

    # Text related methods
    def start_text_on(self, k):
        pass

    def update_text_on(self, k):
        pass

    def end_text_on(self, k):
        pass

    def refresh(self):
        if self.window:
            self.window.noutrefresh()
