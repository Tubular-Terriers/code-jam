import pymunk

from .. import category, collision_type
from .entity import Entity
from .entity_type import EntityType


class Ball(Entity, pymunk.Body):
    def __init__(self, uuid=None):
        Entity.__init__(self, EntityType.PLAYER, uuid)
        pymunk.Body.__init__(self, mass=1, moment=1, body_type=pymunk.Body.DYNAMIC)

        self.circle = pymunk.Circle(self, 1)
        self.circle.filter = pymunk.ShapeFilter(
            categories=category.BALL, mask=category.MASK.BALL
        )

        self.circle.elasticity = 1.0
        self.circle.friction = 0

        self.circle.collision_type = collision_type.BALL

        self.tuple = self, self.circle

        self.ownerUUID = None

    def add_space(self, space):
        space.add(*self.tuple)
