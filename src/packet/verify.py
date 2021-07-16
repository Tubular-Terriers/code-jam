import json

from ._packet import Packet


class Verify(Packet):
    ACTION = "verify"

    def __init__(self, token):
        super().__init__(self.ACTION)
        self.token = token

    def dump(self):
        return {"TOKEN": self.token}

    @staticmethod
    def load(payload) -> object:
        return Verify(payload["TOKEN"])
