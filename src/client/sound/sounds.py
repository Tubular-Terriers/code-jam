import os
import random
from enum import Enum

filepath = os.path.dirname(__file__)


class SoundEffects(Enum):
    PADDLE_BOUNCE = os.path.join(
        filepath, "sound_effects/original_pong_sounds/paddle_bounce.mp3"
    )
    WALL_BOUNCE = os.path.join(
        filepath, "sound_effects/original_pong_sounds/wall_bounce.mp3"
    )
    SCORE = os.path.join(filepath, "sound_effects/original_pong_sounds/score.mp3")


class Music(Enum):
    MENU = random.choice(
        [
            os.path.join(filepath, "music/menu/military.mp3"),
            os.path.join(filepath, "music/menu/cyberpunk_midtempo.mp3"),
        ]
    )
    LOADING = os.path.join(filepath, "music/loading_screen/true_grit.mp3")
    BACKGROUND = [
        os.path.join(filepath, "music/retro/retro.mp3"),
        os.path.join(filepath, "music/retro/vintage_retro.mp3"),
        os.path.join(filepath, "music/retro/60s_summer.mp3"),
        os.path.join(filepath, "music/retro/retro_arcade_80s.mp3"),
        os.path.join(filepath, "music/retro/retro_instrumental.mp3"),
        os.path.join(filepath, "music/retro/retro_the_road.mp3"),
    ]
