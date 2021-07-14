from ._event import Event


class MoveBar(Event):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(self, value):
        super().__init__("MOVE_PLAYER", value)
