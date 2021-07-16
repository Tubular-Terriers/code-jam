import json

from ._packet import Packet


class VerifyResponse(Packet):
    ACTION = "verify_response"

    def __init__(self, is_ok, error=None):
        super().__init__(self.ACTION)
        self.payload = {"status": is_ok}
        if not error:
            self.payload["error"] = error

    def dump(self):
        return json.dumps({"TOKEN": self.token})

    @staticmethod
    def load(payload) -> object:
        return VerifyResponse.__init__(payload["status"] == "OK", payload.get("error"))
