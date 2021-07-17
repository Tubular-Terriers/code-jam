import pymunk
import random
import math

from .. import category, collision_type
from .entity import Entity
from .entity_type import EntityType
from .ball import Ball
from .._objects import border


class Border(Entity, pymunk.Body):
    def __init__(self, x1, y1, x2, y2, uuid=None):
        Entity.__init__(self, EntityType.BORDER, uuid)
        pymunk.Body.__init__(self, mass=1, moment=1, body_type=pymunk.Body.KINEMATIC)
        self.icoords = x1, y1
        self.fcords = x2, y2
        self.border = border(self._body, x1, y1, x2, y2)
        self.borderelasticity = 1
        self.border.friction = 0
        self.border.collision_type = collision_type.BORDER
        self.border.filter = pymunk.ShapeFilter(
            categories=category.BORDER, mask=category.MASK.BORDER
        )
        self.tuple = self, self.border

    def add_space(self, space, object=None):
        space.add(*self.tuple)

    def get_segment(self):
        return self.border

    def inside(self, *coords):
        cx, cy = coords
        bix, biy = self.icoords
        bfx, bfy = self.fcords
        chsum = ()
        if cx > bfx:
            chsum[0] = 1
        elif cx < bix:
            chsum[0] = -1
        else:
            chsum[0] = 0

        if cy > bfy:
            chsum[1] = 1
        elif cy < biy:
            chsum[1] = -1
        else:
            chsum[1] = 0

        print(chsum)
