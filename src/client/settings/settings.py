from enum import Enum, auto


class Settings(Enum):
    MUSIC_VOLUME = auto()
    SFX_VOLUME = auto()
    DECREASE_VOLUME_DURING_GAME_PAUSE = auto()
    GAME_PAUSE_NORMAL_VOLUME_PERCENTAGE = auto()
    MUTE_GAME_ON_FOCUS_LOSS = auto()
