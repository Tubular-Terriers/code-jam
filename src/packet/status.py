import json

from ._packet import Packet


class Status(Packet):
    ACTION = "status"

    def __init__(self, status, error=None, uuid=1):
        super().__init__(self.ACTION, uuid)
        self.status = status
        self.error = error

    def dump(self):
        p = {"status": "OK" if self.status else "ERROR"}
        if self.error:
            p["error"] = self.error
        return p

    @staticmethod
    def load(payload) -> object:
        return Status.__init__((payload.status == "OK"), payload.get("error", None))
