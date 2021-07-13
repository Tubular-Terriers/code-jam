# Write static prestes for rich presence here

from enum import Enum


class RichPresenceDetails(Enum):
    MAIN_MENU = "In main menu"
    LOADING = "Joining server"
    PLAYING = "In game"
    PAUSED = "Game paused"
    GAME_OVER = "Game lost"
    GAME_WON = "Game won"
