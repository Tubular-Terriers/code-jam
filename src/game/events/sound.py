from enum import auto

from ._event import Event


class Sound(Event):
    WALL_BOUNCE = 0
    PADDLE_BOUNCE = 1
    PLAYER_DAMAGE = 2
    ID = "SOUND"

    def __init__(self, value):
        super().__init__(self.ID, value)
