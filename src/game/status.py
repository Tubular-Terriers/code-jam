# Game codes reported by the game
from enum import Enum


class Description:
    def __init__(self, msg, description=""):
        self.msg = msg
        self.description = description

    def __repr__(self):
        return f"<Description object msg={repr(self.msg)} description={repr(self.description)}>"

    def __str__(self):
        return f"{self.msg}\n{self.description}"


class Status(Enum):
    START_SUCCESS = Description("The game started successfully!")
    START_ALREADY_RUNNING = Description("The game is already running")
    STOP_SUCCESS = Description("The game stopped successfully!")
    STOP_NOT_RUNNING = Description("The game is not running")
