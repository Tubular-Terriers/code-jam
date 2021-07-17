import pymunk
import random
import math

from .. import category, collision_type
from .entity import Entity
from .entity_type import EntityType
from .ball import Ball


class Spawner(Entity, pymunk.Body):
    def __init__(self, cooldown=1000, uuid=None):
        Entity.__init__(self, EntityType.SPAWNER, uuid)
        pymunk.Body.__init__(self, mass=1, moment=1, body_type=pymunk.Body.STATIC)
        self.direction = None
        self.cooldown = cooldown
        self.timeout = cooldown
        self.SPAWN_ANGLE = 120
        self.magnitude = 70
        self.tuple = (self,)

    def add_space(self, space, object=None):
        if object is not None:
            # add the ball to the space
            return
        space.add(*self.tuple)

    def spawn_ball(
        self, space, w, h, callback=None
    ):  # with velocity between a given angle and direction
        # spawn it not only if cools down but if ball gets destroyed as well
        if self.is_cooled():
            print("spawned a ball")

            θ1, θ2 = 0, self.SPAWN_ANGLE

            tθ1, tθ2 = θ1 - self.SPAWN_ANGLE / 2, θ2 - self.SPAWN_ANGLE / 2

            dθ = random.uniform(tθ1, tθ2)
            dx = random.choice([1, -1])

            ball = Ball()
            ball.position = (w // 2, h // 2)
            ball.velocity = (
                math.cos(math.radians(dθ)) * dx * self.magnitude,
                math.sin(math.radians(dθ)) * self.magnitude,
            )

            ball.add_space(space)
            if callback is not None:
                callback(ball)
            self.cooldown = self.timeout

    def cool(self):
        self.cooldown -= 1

    def is_cooled(self):
        return self.cooldown <= 0
