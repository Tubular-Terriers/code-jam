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

cooldown = 5

time.sleep(cooldown)

music_engine.update_game_state(GameState.LOADING)

time.sleep(cooldown)

music_engine.update_game_state(GameState.PLAYING)

time.sleep(cooldown)

music_engine.update_game_state(GameState.PAUSED)

time.sleep(cooldown)

music_engine.update_game_state(GameState.PLAYING)

sfx_engine.play_sound(SoundEffects.SCORE)
sfx_engine.set_volume(5)

while True:
    music_engine.check_music_end()
    time.sleep(random.randint(0, 5))
    
    if random.randint(0, 5) == 2:
        sfx_engine.play_sound(SoundEffects.SCORE)
    else:
        sfx_engine.play_sound(SoundEffects.PADDLE_BOUNCE)
