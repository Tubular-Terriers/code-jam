import json


class Packet:
    """Interface class. Only send() creates a packet with action name"""

    def __init__(self, action_name: str):
        self.action_name = action_name

    def dump(self):
        """Dumps the data to payload json form"""
        raise NotImplementedError

    @staticmethod
    def load(data) -> object:
        """Loads the data from payload json"""
        raise NotImplementedError

    def send(self) -> str:
        """Returns a json packet to send"""
        json.dumps(
            {
                "action": self.action_name,
                "payload": self.dump(),
            }  # self.dump() must be implemented
        )
