from ._event import Event


class Sound(Event):
    HIT = "SOUND_BALL_HIT"
    PLAYER_DAMAGE = "SOUND_PLAYER_DAMAGE"
    ID = "SOUND"

    def __init__(self, value):
        super().__init__(self.ID, value)
