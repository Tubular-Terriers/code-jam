import json

from ._packet import Packet


class Verify(Packet):
    ACTION = "verify"

    def __init__(self, token):
        super().__init__(self.ACTION)
        self.token = token

    def dump(self):
        return json.dumps({"TOKEN": self.token})

    @staticmethod
    def load(data) -> object:
        return Verify.__init__(data["TOKEN"])
