import pymunk

from .. import category
from ..events import MoveBar, MovePlayer
from .entity import Entity
from .entity_type import EntityType


class Player(Entity, pymunk.Body):
    def __init__(self, uuid=None):
        Entity.__init__(self, EntityType.PLAYER, uuid)
        pymunk.Body.__init__(self, mass=1, moment=1, body_type=pymunk.Body.DYNAMIC)
        self.name = "test player"

        # ---|||||--------- height
        # width

        width = 40
        height = 8

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

        self.tuple = self, self.bounding_box  # , self.ball_collision_box, self.hitbox

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

    def process_bar_direction(self, dir):
        """`dir` is a type of MoveBar"""

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
