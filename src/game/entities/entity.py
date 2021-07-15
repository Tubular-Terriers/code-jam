from uuid import uuid4

from .entity_type import EntityType


class Entity:
    def __init__(self, type: EntityType, uuid):
        self.uuid = uuid if uuid else uuid4()
        self.type = type
