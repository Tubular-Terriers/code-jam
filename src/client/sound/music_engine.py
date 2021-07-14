import random

import pygame
from pygame import mixer
from sounds import Music

from src.game.archive.game_state import GameState


class MusicEngine:
    def __init__(
        self,
        game_paused_volume_percentage: int,
        default_volume: int,
        mixer_channels: int = 64,
    ):
        mixer.pre_init()
        mixer.init()
        pygame.init()
        mixer.set_num_channels(mixer_channels)
        self.mixer_channels = mixer_channels
        self.current_track = None
        self.previous_track = None
        self._game_state_ = None
        self._previous_game_state_ = None
        self._volume_ = default_volume
        self._music_ = mixer.music
        self.set_volume(self._volume_)
        self._game_paused_volume_ = (
            game_paused_volume_percentage * self._volume_
        ) / 100
        self._music_end_ = pygame.event.custom_type()

    def set_volume(self, volume: int) -> None:
        self._volume_ = volume / 100
        self._music_.set_volume(self._volume_)

    def set_game_paused_volume(self, volume: int) -> None:
        self._game_paused_volume_ = volume / 100
        if self._game_state_ == GameState.PAUSED:
            self._music_.set_volume(self._game_paused_volume_)

    def update_game_state(self, game_state) -> None:
        self._previous_game_state_ = self._game_state_
        self._game_state_ = game_state
        self._refresh_()

    def _refresh_(self) -> None:
        if self._game_state_ is GameState.MAIN_MENU:
            self._music_.stop()
            self._music_.load(Music.MENU.value)
            self._music_.play(-1)

        elif self._game_state_ is GameState.LOADING:
            self._music_.stop()
            self._music_.load(Music.LOADING.value)
            self._music_.play(-1)

        elif self._game_state_ is GameState.PLAYING:
            if self._previous_game_state_ is GameState.PAUSED:
                self._music_.set_volume(self._volume_)
            else:
                self._music_.stop()
                self.current_track = random.choice(Music.BACKGROUND.value)
                self._music_.load(self.current_track)
                self._music_.play()
                self._music_.set_endevent(self._music_end_)

        elif self._game_state_ is GameState.PAUSED:
            self._music_.set_volume(self._game_paused_volume_)

        elif self._game_state_ is GameState.GAME_WON:
            pass  # TODO: Add

        elif self._game_state_ is GameState.GAME_OVER:
            pass  # TODO: Add

    def check_music_end(self) -> None:
        for event in pygame.event.get(eventtype=self._music_end_):
            if event.type == self._music_end_:
                self._play_next_song_()

    def _play_next_song_(self) -> None:
        self.previous_track = self.current_track
        new_tracks_list = [
            track for track in Music.BACKGROUND.value if track != self.previous_track
        ]
        self.current_track = random.choice(new_tracks_list)

        self._music_.load(self.current_track)
        self._music_.play()
