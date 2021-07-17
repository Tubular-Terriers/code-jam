import json
from uuid import uuid4


class Packet:
    """Interface class. Only send() creates a packet with action name"""

    def __init__(self, action_name: str, uuid=None):
        """Set `uuid` to 0 to auto generate a packet id

        pass in 1 from the super class's uuid parameter to enforce a uuid when
        creating a send packet
        """
        self.action_name = action_name
        self.client_id = None
        if uuid == 0:
            self.packet_id = uuid4()
        else:
            self.packet_id = uuid

    def dump(self):
        """Dumps the data to `dict`"""
        raise NotImplementedError

    @staticmethod
    def load(payload) -> object:
        """Loads the data from dict(payload)"""
        raise NotImplementedError

    def send(self) -> str:
        """Returns a json packet to send"""
        if self.packet_id == 1:
            raise Exception("The super packet class requires a uuid to send")
        p = {
            "action": self.action_name,
            "payload": self.dump(),
        }  # self.dump() must be implemented
        if self.packet_id:
            p["packet_id"] = str(self.packet_id)
        if self.client_id:
            p["client_id"] = str(self.client_id)
        return json.dumps(p)
