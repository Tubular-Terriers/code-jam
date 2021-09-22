import json

from ._packet import Packet


class GamePacket(Packet):
    ACTION = "game"

    def __init__(self, events=None, entities=None):
        super().__init__(self.ACTION)
        if events is None:
            events = {}
        if entities is None:
            entities = []
        self.events = events
        self.entities = entities

    def dump(self):
        return {"events": self.events, "entities": self.entities}

    @staticmethod
    def load(payload) -> object:
        return GamePacket.__init__(payload["events"], payload["entities"])
