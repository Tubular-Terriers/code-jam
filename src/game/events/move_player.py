from ._event import Event


class MovePlayer(Event):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(self, value):
        super().__init__("MOVE_PLAYER", value)
