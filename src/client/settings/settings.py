from enum import Enum


class Settings(Enum):
    MUSIC_VOLUME = "music_volume"
    SFX_VOLUME = "sfx_volume"
    DECREASE_VOLUME_DURING_GAME_PAUSE = "decrease_volume_during_game_pause"
    GAME_PAUSE_NORMAL_VOLUME_PERCENTAGE = "game_pause_normal_volume_percentage"
    MUTE_GAME_ON_FOCUS_LOSS = "mute_game_on_focus_loss"
