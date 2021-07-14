import pymunk

from ..events import MoveBar, MovePlayer
from .entity import Entity
from .entity_type import EntityType


class Player(Entity, pymunk.Body):
    def __init__(self):
        Entity.__init__(self, EntityType.PLAYER)
        pymunk.Body.__init__(self, body_type=pymunk.Body.STATIC)
        self.name = "test player"
        self.uuid = None

        # ---|||||--------- height
        # width

        width = 40
        height = 4

        self.bar_loc = 0
        # Value between 1 to -1. 1
        # 1 represents right/top
        # -1 represents left/bottom

        self.horizontal = True

        # create rectangle player box
        self.player_box = pymunk.Poly(
            self,
            [
                (-width / 2, -height / 2),
                (width / 2, -height / 2),
                (width / 2, height / 2),
                (-width / 2, height / 2),
            ],
        )

        self.tuple = self, self.player_box

    def process_move_direction(self, dir):
        """`dir` is a type of MovePlayer"""

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
