# include net delta reconstructors and validations as well
import asyncio

import events
import pymunk
from status import Status


class Game:
    def __init__(self):
        # TODO: make these customizable
        self.width = 600
        self.height = 600
        # 20 as default
        self.tickrate = 20

        # Enitialize the simulation environment
        self.space = pymunk.Space((self.width, self.height))
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
        if "debug":
            import render

            self.render = render.Renderer(self.space)

        # TODO: make this an option
        self.running = False

        self.coroutine = None

    # Process an event
    def process(self):
        pass

    async def loop(self):
        while True:
            print("ticking")
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
