from ._event import Event


class MoveBar(Event):
    UP = "BAR_UP"
    DOWN = "BAR_DOWN"
    LEFT = "BAR_LEFT"
    RIGHT = "BAR_RIGHT"
    ID = "BAR_MOVE_BAR"

    def __init__(self, value):
        super().__init__(self.ID, value)
