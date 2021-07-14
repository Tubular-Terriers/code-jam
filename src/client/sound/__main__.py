import random
import time

from music_engine import MusicEngine
from sound_effects_engine import SoundEffectsEngine

from src.client.sound.sounds import SoundEffects
from src.game.archive.game_state import GameState

# settings.sfx_volume
sfx_engine = SoundEffectsEngine(100)
# TODO: Implement settings
# settings.game_paused_volume, settings.music_volume
music_engine = MusicEngine(20, 10)

music_engine.update_game_state(GameState.MAIN_MENU)

time.sleep(5)

music_engine.update_game_state(GameState.LOADING)

time.sleep(5)

music_engine.update_game_state(GameState.PLAYING)

time.sleep(5)

music_engine.update_game_state(GameState.PAUSED)

time.sleep(5)

music_engine.update_game_state(GameState.PLAYING)

score_snd = sfx_engine.create_sound(SoundEffects.SCORE)
wall_bounce_snd = sfx_engine.create_sound(SoundEffects.WALL_BOUNCE)

while True:
    music_engine.check_music_end()
    time.sleep(random.randint(0, 5))
    if random.randint(0, 5) == 2:
        score_snd.play()
    else:
        wall_bounce_snd.play()
