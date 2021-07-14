import pymunk

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
