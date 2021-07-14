from ._event import Event


class MoveBar(Event):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ID = "MOVE_BAR"

    def __init__(self, value):
        super().__init__(self.ID, value)
