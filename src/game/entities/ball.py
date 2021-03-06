import random

import pymunk

from .. import category, collision_type
from .entity import Entity
from .entity_type import EntityType


class Ball(Entity, pymunk.Body):
    def __init__(self, uuid=None):
        Entity.__init__(self, EntityType.BALL, uuid)
        pymunk.Body.__init__(self, mass=1, moment=1, body_type=pymunk.Body.DYNAMIC)
        self.BOUNCE_AMOUNT = 3
        self.bounce_count = 0

        self.update_id = random.randint(1, 10)

        self.circle = pymunk.Circle(self, 1)
        self.circle.filter = pymunk.ShapeFilter(
            categories=category.BALL, mask=category.MASK.BALL
        )

        self.circle.elasticity = 1.0
        self.circle.friction = 0

        self.circle.collision_type = collision_type.BALL

        self.tuple = self, self.circle

        self.ownerUUID = None

    def reset(self):
        self.bounce_count = 0
        self.ownerUUID = None
        return True

    def add_space(self, space):
        space.add(*self.tuple)

    def is_last_bounce(self):
        return self.bounce_count == self.BOUNCE_AMOUNT

    def load_data(self, data):
        super().load_data(data)
        self.bounce_count = data["bounce_count"]
        self.update_id = data["update_id"]

    def dump_data(self):
        return {
            **super().dump_data(),
            "update_id": self.update_id,
            "bounce_count": self.bounce_count,
        }
