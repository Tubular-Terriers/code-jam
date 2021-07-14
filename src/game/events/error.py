from ._event import Event


class Error(Event):
    ID = "ERROR"

    def __init__(self, value="No message provided"):
        super().__init__(self.ID, value)
