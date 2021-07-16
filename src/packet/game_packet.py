import json


class GamePacket:
    def __init__(self, events):
        self.events = events

    def dump(self):
        return json.dumps({"events": self.events})

    @staticmethod
    def load(data) -> object:
        return GamePacket.__init__(data["events"])
