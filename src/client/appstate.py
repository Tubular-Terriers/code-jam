from enum import Enum, auto


class AppState(Enum):
    """defining appstates"""

    EXIT = auto()
    MENU = auto()
    MAIN_MENU = auto()
    GAME = auto()
    GAME_OVER = auto()
    SETTINGS_SCR = auto()
    CREDITS_SCR = auto()
    AUTH_SCR = auto()
    HOST_GAME = auto()