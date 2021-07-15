from enum import Enum, auto


class AppState(Enum):
    EXIT = 0
    MENU = 1
    MAIN_MENU = 2
    GAME = 3
    GAME_OVER = 4
    CREDITS_SCR = 5
