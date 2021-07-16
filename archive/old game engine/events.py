# Events used by the game


class GameEvent:
    def __init__(self, name, description, properties):
        self.name = name
        self.description = description
        self.properties = properties
