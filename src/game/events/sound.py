from client.sound.sounds import SoundEffects

from ._event import Event


class Sound(Event):
    WALL_BOUNCE = SoundEffects.WALL_BOUNCE
    PADDLE_BOUNCE = SoundEffects.PADDLE_BOUNCE
    PLAYER_DAMAGE = SoundEffects.SCORE
    ID = "SOUND"

    def __init__(self, value):
        super().__init__(self.ID, value)
