import json

from ._packet import Packet


class Verify(Packet):
    ACTION = "verify"

    def __init__(self, token):
        super().__init__(self.ACTION, uuid=0)
        self.token = token

    def dump(self):
        return {"token": self.token}

    @staticmethod
    def load(payload) -> object:
        return Verify(payload["token"])
