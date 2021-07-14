from enum import Enum, auto


class GameState(Enum):
    MAIN_MENU = auto()
    LOADING = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    GAME_WON = auto()
