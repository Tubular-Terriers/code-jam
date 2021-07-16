import json

from ._packet import Packet


class GamePacket(Packet):
    ACTION = "game"

    def __init__(self, events):
        super().__init__(self.ACTION)
        self.events = events

    def dump(self):
        return json.dumps({"events": self.events})

    @staticmethod
    def load(data) -> object:
        return GamePacket.__init__(data["events"])
