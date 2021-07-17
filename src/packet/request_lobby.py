import json
import re

from ._packet import Packet


class RequestLobby(Packet):
    ACTION = "request_lobby"

    def __init__(self, username=None, password=None, uuid=1):
        """Requires a uuid"""
        super().__init__(self.ACTION, uuid)
        self.username = self.username
        self.password = self.password

    def dump(self):
        payload = {"username": self.username, "password": self.password}
        return payload

    @staticmethod
    def load(payload) -> object:
        return RequestLobby()

    def is_verified(self):
        return self.is_ok

    def validate_username(self):
        if re.match("^[A-Za-z_]{3,8}$", self.username):
            return True
        return False
