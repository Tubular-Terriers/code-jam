import json
import math
from math import copysign

import pymunk

from .. import category, collision_type
from ..events import MoveBar, MovePlayer
from .entity import Entity
from .entity_type import EntityType


class Player(Entity, pymunk.Body):
    def __init__(self, uuid=None):
        Entity.__init__(self, EntityType.PLAYER, uuid)
        pymunk.Body.__init__(self, mass=1, moment=1, body_type=pymunk.Body.DYNAMIC)
        self.name = "test player"

        self.health = 10

        # ---|||||--------- height
        # width

        self.bar_speed = 0.1
        self.bar_loc = 0
        # Value between 1 to -1. 1
        # 1 represents right/top
        # -1 represents left/bottom

        self.horizontal = True

        # create rectangle player box
        # self.player_box = pymunk.Poly(
        #     self,
        #     [
        #         (-width / 2, -height / 2),
        #         (width / 2, -height / 2),
        #         (width / 2, height / 2),
        #         (-width / 2, height / 2),
        #     ],
        # )
        # print(self.friction)
        # self.friction = 0

        # Create bounding box (circle)
        self.bounding_box = pymunk.Circle(self, 22)
        self.bounding_box.filter = pymunk.ShapeFilter(
            categories=category.BOUNDING_BOX, mask=category.MASK.BOUNDING_BOX
        )
        self.bounding_box.collision_type = collision_type.BOUNDING_BOX

        self.hitbox_width = 50

        def hb_fact(w, h):
            b = pymunk.Segment(self, (-w / 2, -h / 2), (w / 2, h / 2), 0.5)
            b.collision_type = collision_type.HITBOX
            b.filter = pymunk.ShapeFilter(
                categories=category.HITBOX, mask=category.MASK.HITBOX
            )
            return b

        self.hitbox_vert = hb_fact(self.hitbox_width, 0)
        self.hitbox_hori = hb_fact(0, self.hitbox_width)

        ##################################################
        # This is a whole different body on top of player
        self.bcb_body = pymunk.Body(1, 1, pymunk.Body.KINEMATIC)
        bcb_width = 8
        bcb_height = 5
        self.bcb_range = (self.hitbox_width - bcb_width + 2) / 2
        self.ball_collision_box = pymunk.Poly(
            self.bcb_body,
            [
                (-bcb_width / 2, -bcb_height / 2),
                (bcb_width / 2, -bcb_height / 2),
                (bcb_width / 2, bcb_height / 2),
                (-bcb_width / 2, bcb_height / 2),
            ],
        )

        self.tuple = self.shapes, self.bcb_body.shapes

        self.ball_collision_box.collision_type = collision_type.BALL_COLLISION_BOX
        self.ball_collision_box.filter = pymunk.ShapeFilter(
            categories=category.BALL_COLLISION_BOX,
            mask=category.MASK.BALL_COLLISION_BOX,
        )
        self.ball_collision_box.elasticity = 1

        self.bb = self, self.bounding_box, self.hitbox_vert, self.hitbox_hori
        self.bcb = (
            self.ball_collision_box,
            self.bcb_body,
        )

    def add_space(self, space):
        space.add(pymunk.constraints.RotaryLimitJoint(space.static_body, self, 0, 0))
        space.add(*self.bb)
        space.add(*self.bcb)

    def reset(self):
        pass

    def bleed(self):
        self.health -= 1

    def process_move_keys(self, keys: dict):
        """`dir` is a type of MovePlayer"""
        xv = 0
        yv = 0
        if keys[MovePlayer.UP]:
            yv -= 50
        if keys[MovePlayer.DOWN]:
            yv += 50
        if keys[MovePlayer.LEFT]:
            xv -= 50
        if keys[MovePlayer.RIGHT]:
            xv += 50
        self.velocity = (xv, yv)

    def process_bar_keys(self, keys: dict):
        """`dir` is a type of MoveBar"""
        bar_vert = 0
        bar_hori = 0
        if keys[MoveBar.UP]:
            bar_vert -= 1
        if keys[MoveBar.DOWN]:
            bar_vert += 1
        if keys[MoveBar.LEFT]:
            bar_hori -= 1
        if keys[MoveBar.RIGHT]:
            bar_hori += 1
        # Prioritize left right
        # The code below adds a game mechanic called
        # "Rotation" which basically makes
        # Orientation changing intuitive
        if bar_vert != 0:
            # Move the bar vertically
            if self.horizontal:
                # Align the bar first
                self.bar_loc = copysign(self.bar_loc, bar_vert)
            # Apply the position change
            self.bar_loc += copysign(self.bar_speed, bar_vert)
            self.horizontal = False
        elif bar_hori != 0:
            # Move the bar horizontally
            if not self.horizontal:
                # Align the bar first
                self.bar_loc = copysign(self.bar_loc, bar_hori)
            # Apply the position change
            self.bar_loc += copysign(self.bar_speed, bar_hori)
            self.horizontal = True
        # Bound the bar to -1~1
        self.bar_loc = max(-1, min(self.bar_loc, 1))

    def _update_bar(self) -> None:
        """Updates the position of bar based on `horizontal` and `bar_loc`"""
        if self.horizontal:
            self.bcb_body.angle = 0
            dx = self.bar_loc * self.bcb_range
            self.bcb_body.position = (self.position[0] + dx, self.position[1])
        else:
            self.bcb_body.angle = math.pi * 0.5
            dy = self.bar_loc * self.bcb_range
            self.bcb_body.position = (self.position[0], self.position[1] + dy)

    def _set_vertical(self) -> None:
        if self.horizontal:
            self.bar_loc = 0
            self.horizontal = False

    def _set_horizontal(self) -> None:
        if not self.horizontal:
            self.bar_loc = 0
            self.horizontal = True

    def tick(self, callback):
        """Callback"""

    def load_data(self, data):
        data = json.loads(data)
        super().load_data(data)

    def dump_data(self):
        data = {**super().dump_data()}
        return data
