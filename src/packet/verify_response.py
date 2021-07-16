import json

from ._packet import Packet


class VerifyResponse(Packet):
    ACTION = "verify_response"

    def __init__(self, is_ok, error=None):
        super().__init__(self.ACTION)
        self.is_ok = is_ok
        self.error = error

    def dump(self):
        payload = {"status": self.is_ok}
        if not self.error:
            payload["error"] = self.error
        return payload

    @staticmethod
    def load(payload) -> object:
        return VerifyResponse(
            "OK" if payload["status"] else "ERROR", payload.get("error")
        )

    def is_verified(self):
        return self.is_ok
