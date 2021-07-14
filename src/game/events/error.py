from ._event import Event


class Error(Event):
    def __init__(self, value="No message provided"):
        super().__init__("ERROR", value)
