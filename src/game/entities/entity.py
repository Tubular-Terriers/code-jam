from .entity_type import EntityType


class Entity:
    def __init__(self, type: EntityType):
        self.type = type
