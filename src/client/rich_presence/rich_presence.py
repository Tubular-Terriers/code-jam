import time
from enum import Enum, auto
from os import environ, getpid

from dotenv import load_dotenv
from pypresence import Client

from .__static__ import RichPresenceDetails


class RichPresenceState(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()


class RichPresence:
    def __init__(self, loop):
        load_dotenv()
        self._client_id_ = environ.get("client_id")
        self._rich_presence_client_ = Client(self._client_id_, loop=loop)
        self.state = RichPresenceState.DISCONNECTED

    def start_connection(self):
        self._rich_presence_client_.start()
        self.state = RichPresenceState.CONNECTED

    def end_connection(self):
        self._rich_presence_client_.close()
        self.state = RichPresenceState.DISCONNECTED

    def update_activity(
        self,
        pid: int = getpid(),
        state: str = None,
        details: str = None,
        start: int = None,
        end: int = None,
        large_image: str = None,
        large_text: str = None,
        small_image: str = None,
        small_text: str = None,
        party_id: str = None,
        party_size: list = None,
        join: str = None,
        spectate: str = None,
        match: str = None,
        buttons: list = None,
        instance: bool = True,
    ):
        return self._rich_presence_client_.set_activity(
            pid,
            state,
            details,
            start,
            end,
            large_image,
            large_text,
            small_image,
            small_text,
            party_id,
            party_size,
            join,
            spectate,
            match,
            buttons,
            instance,
        )

    def clear_activity(self, pid: int = getpid()):
        self._rich_presence_client_.clear_activity(pid)

    def __repr__(self):
        return f"<RichPresence object state = {self.state.value}>"


if __name__ == "__main__":
    r = RichPresence()
    r.start_connection()
    r.update_activity(
        details="Playing online multiplayer",
        state="Competitive",
        start=int(time.time()),
        end=int(time.time() + 120),
        party_size=[2, 4],
    )

    while True:
        time.sleep(15)
