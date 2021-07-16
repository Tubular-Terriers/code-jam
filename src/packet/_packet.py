class Packet:
    """Interface class"""

    def __init__(self):
        pass

    def dump(self):
        """Dumps the data to payload json form"""
        raise NotImplementedError

    @staticmethod
    def load(data):
        """Loads the data from payload json"""
        raise NotImplementedError
