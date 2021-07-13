import os
import random
from enum import Enum

filepath = os.path.dirname(__file__)


class SoundEffects(Enum):
    PADDLE_BOUNCE = os.path.join(
        filepath, "sound_effects/original_pong_sounds/paddle_bounce.ogg"
    )
    WALL_BOUNCE = os.path.join(
        filepath, "sound_effects/original_pong_sounds/wall_bounce.ogg"
    )
    SCORE = os.path.join(filepath, "sound_effects/original_pong_sounds/score.ogg")


class Music(Enum):
    MENU = os.path.join(filepath, "music/tetris/tetris_theme.ogg")
    LOADING = random.choice(
        [
            os.path.join(filepath, "music/loading_screen/military.ogg"),
            os.path.join(filepath, "music/loading_screen/cyberpunk_midtempo.ogg"),
            os.path.join(filepath, "music/loading_screen/true_grit.ogg"),
        ]
    )
    BACKGROUND = [
        os.path.join(filepath, "music/retro/retro.ogg"),
        os.path.join(filepath, "music/retro/vintage_retro.ogg"),
        os.path.join(filepath, "music/retro/60s_summer.ogg"),
        os.path.join(filepath, "music/retro/retro_arcade_80s.ogg"),
        os.path.join(filepath, "music/retro/retro_instrumental.ogg"),
        os.path.join(filepath, "music/retro/retro_the_road.ogg"),
    ]
