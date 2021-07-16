from pygame import mixer
from .sounds import SoundEffects
from game.events.sound import Sound


class SoundEffectsEngine:
    def __init__(self, default_volume: int, mixer_channels: int = 64):
        mixer.pre_init()
        mixer.init()
        mixer.set_num_channels(mixer_channels)
        self.mixer_channels = mixer_channels
        self._volume_ = default_volume / 100

        self._sounds_ = {}

        for sound_effect in SoundEffects:
            sound = mixer.Sound(sound_effect.value)
            sound.set_volume(self._volume_)
            self._sounds_[sound_effect.value] = sound

    def play_sound(self, sound: SoundEffects) -> None:
        self._sounds_[sound.value].play()

    def set_volume(self, volume: int) -> None:
        self._volume_ = volume / 100
        for sound in self._sounds_.values():
            sound.set_volume(self._volume_)

    def process(self, event_name, event_value):
        if event_name == Sound.ID:
            self.play_sound(event_value)
