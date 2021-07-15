from uuid import uuid4

from .entity_type import EntityType


class Entity:
    def __init__(self, type: EntityType, uuid):
        self.uuid = uuid if uuid else uuid4()
        self.type = type

    # Partial
    def load_data(self, data):
        """Remember to do `data = json.loads(data)`"""
        self.position = data["position"]
        self.velocity = data["velocity"]
        self.angular_velocity = data["angular_velocity"]
        self.angle = data["angle"]

    # Partial
    def dump_data(self):
        """Remember to return a `json.dumps()`"""
        return {
            "position": self.position,
            "velocity": self.velocity,
            "angular_velocity": self.angular_velocity,
            "angle": self.angle,
        }
