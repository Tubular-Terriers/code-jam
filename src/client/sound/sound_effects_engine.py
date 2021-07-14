from pygame import mixer
from sounds import SoundEffects


class SoundEffectsEngine:
    def __init__(self,
                 default_volume: int,
                 mixer_channels: int = 64):
        mixer.pre_init()
        mixer.init()
        mixer.set_num_channels(mixer_channels)
        self.mixer_channels = mixer_channels
        self._volume_ = default_volume / 100
        
    def create_sound(self, sound: SoundEffects):
        new_sound = mixer.Sound(sound.value)
        new_sound.set_volume(self._volume_)
        return new_sound
