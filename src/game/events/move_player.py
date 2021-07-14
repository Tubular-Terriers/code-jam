from ._event import Event


class MovePlayer(Event):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ID = "MOVE_PLAYER"

    def __init__(self, value):
        super().__init__(self.ID, value)
