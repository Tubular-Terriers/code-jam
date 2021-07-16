# include net delta reconstructors and validations as well
import asyncio

import events
import pygame
import pymunk
from entity_manager import EntityManager
from map.map_manager import MapManager
from render.render_engine import RenderEngine
from status import Status


class Game:
    def __init__(self, entities, space):
        # TODO: make these customizable
        self.width = 600
        self.height = 600
        # 20 as default
        self.tickrate = 20
        self.objects = {}
        self.entities = entities
        # Enitialize the simulation environment
        self.space = space
        self.space.gravity = 0, 0

        # TEMP CODE######################################
        self.space.gravity = 0, 5

        b0 = self.space.static_body
        segment = pymunk.Segment(b0, (0, 238), (640, 238), 4)
        segment.elasticity = 1

        body = pymunk.Body(mass=1, moment=10)
        body.position = 100, 200

        circle = pymunk.Circle(body, radius=20)
        circle.elasticity = 0.95

        self.space.add(body, circle, segment)
        # TEMP CODE###########################

        # TODO add launch debug option
        # if "debug":
        #   import render
        #    self.render = render.Renderer(self.space)

        # TODO: make this an option
        self.running = False

        self.coroutine = None

    # Process an event
    def process(self):
        pass

    def parse_entities(self):
        for i in self.entities:
            entity = self.entities[i]
            print(pymunk.Segment(space, (0, 0), (50, 40), radius=10))
            type = entity["type"]
            if type not in self.objects:
                self.objects[type] = []
            if type == "o":
                self.objects[type].append(entity)
        return True

    def get_objects(self):
        return self.objects

    async def loop(self):
        while True:
            self.tick()
            # TODO: Fix this to dynamically sleep that compensates the tick time
            await asyncio.sleep(1 / self.tickrate)

    # Do a game step
    def tick(self):
        self.space.step(0.05)

    # TODO: do the Status.START thing
    def start(self):
        # fff
        self.coroutine = asyncio.create_task(self.loop)

    """
    returns a state code
    """

    def stop(self):
        pass

    def is_running(self):
        if self.coroutine is not None:
            return True
        return False


space = pymunk.Space()
space.gravity = 0, 0
mapmng = MapManager()
print(
    mapmng.set_level(
        0,
        """
            -----oooo-oo-oooo---
            --ppp-----o--oo--o--""",
    )
)
mapmng.parse(0)
renderer = RenderEngine(" ", 30, 30, True)
enmng = EntityManager(mapmng.get_raw_level(0), renderer)
enmng.parse()

game = Game(enmng.get_entities(), space)
game.parse_entities()
print(game.get_objects())

pygame.quit()
