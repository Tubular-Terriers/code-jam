import asyncio

from client.settings.config import Config
from client.settings.settings import Settings
from client.sound.sound_effects_engine import SoundEffectsEngine  # whatever u did here
from game.engine import Engine

# from client.sound.music_engine import MusicEngine TODO: Add music engine

engine = Engine(debug=True)

settings = Config()
sfx_engine = SoundEffectsEngine(int(settings.get(Settings.SFX_VOLUME)))
# music_engine = MusicEngine(settings.get(Settings.GAME_PAUSE_NORMAL_VOLUME_PERCENTAGE),
#                            settings.get(Settings.MUSIC_VOLUME))

engine.hook(sfx_engine.process)

asyncio.get_event_loop().create_task(engine.run())

asyncio.get_event_loop().run_forever()
