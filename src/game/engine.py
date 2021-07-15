import asyncio
import random
import time
import traceback

import pygame
import pymunk
import pymunk.pygame_util

from . import category
from .entities.ball import Ball
from .entities.player import Player
from .events import Error, MoveBar, MovePlayer


class Engine:
    def __init__(self, debug=False):
        """Does not run until `#run` is called"""
        self.created_timestamp = time.time()
        self.running = True
        self.debug_render = None
        self.tickcount = 0

        self._hooks = {}
        self._hooks[self.process_event] = self.process_event

        self.width = 600
        self.height = 600

        # Game engine tick rate
        self.tps = 100
        # Controller tick rate
        # ticks to controller
        # a value of 5 would mean it will poll the controller every 5th tick
        self.ttc = 5

        self.ttc_tick = 0

        self.space = pymunk.Space()
        self.space.gravity = 0, 0

        self.space.static_body.filter = pymunk.ShapeFilter(
            categories=category.WALL, mask=category.MASK.WALL
        )

        # b = pymunk.Body(1, 1)
        # self.space.add(b)
        # c = pymunk.Circle(b, 10)
        # b.position = (100, 100)
        # self.space.add(c)

        # print(b, c)

        p = Player()
        self.player = p
        p.position = (100, 200)
        self.space.add(*p.tuple)

        self.balls = []
        try:
            for i in range(20):
                ball = Ball()
                ball.position = (10 * i, 300)
                ball.velocity = (0, 100)
                ball.angular_velocity = random.random() * 1000
                self.space.add(*ball.tuple)
                self.balls.append(ball)
        except Exception as e:
            print(e)

        # Test bounding box
        bb = pymunk.BB(50, 300, 150, 150)
        # self.space.add(bb)

        self.load_mapdata()

        # Add custom tick method so debug has an option to use it
        self.control = lambda _=0: 0

        if debug:

            # Process callbacks
            def process_key(key):
                """Process key events passed from pygame window"""
                if key == pygame.SPACE:
                    print("space pressed")

            # Process routines
            def routine():
                try:
                    p = pygame.key.get_pressed()
                    keys = {}
                    keys[MovePlayer.UP] = p[pygame.K_w]
                    keys[MovePlayer.DOWN] = p[pygame.K_s]
                    keys[MovePlayer.LEFT] = p[pygame.K_a]
                    keys[MovePlayer.RIGHT] = p[pygame.K_d]
                    self._emit(MovePlayer.ID, keys)
                except Exception as e:
                    print(e)
                    self._emit(Error.ID, e.message)

            self.control = routine
            self.debug_render = DebugRender(self.space, self.destroy, process_key)

        def on_collision(arbiter, space, data):
            for c in arbiter.contact_point_set.points:
                # check stuff
                print("contact")

    def load_mapdata(self):
        """
        We are NOT going to pass this through websockets. TLDR; downloading maps is impossible

        This is a method for dividing up modules so code does not get clogged up
        """
        from .default_map import data

        for obj in data:
            # Load the objects into space
            # These are all static objects
            obj.body = self.space.static_body

            # Make these bouncy
            obj.elasticity = 1
            obj.friction = 0
            self.space.add(obj)

    async def run(self):
        self.run_task = asyncio.get_event_loop().create_task(self.run_loop())

    async def run_loop(self):
        try:
            while self.running:
                t = time.time()
                self.tick()
                # Compensate for the calculation time in tick
                await asyncio.sleep(t - time.time() + 1 / self.tps)
        except asyncio.CancelledError:
            print("run loop is terminated")

    def tick(self):
        # Update global tick count
        self.tickcount += 1

        # Do controller
        self.ttc_tick += 1
        if self.ttc_tick == self.ttc:
            self.control()
            self.ttc_tick = 0
        self.space.step(1 / self.tps)

        # Do balls
        # for b in self.balls:
        #     b.angular_velocity += 1 / self.tps

    def destroy(self):
        if self.debug_render:
            self.debug_render.destroy()
        if self.run_task:
            self.run_task.cancel()
        print("game exit")

        ##########################
        # REMOVE THIS LINE
        asyncio.get_event_loop().stop()

    ###########################
    # Process events from any other code

    def process_event(self, n, v):
        if MovePlayer.ID == n:
            self._move_player_keys(v)
        elif MoveBar.ID == n:
            self._move_bar_keys(v)

    ############################
    # Events

    def _move_player_keys(self, keys) -> None:
        """`keys` dict where [MovePlayer.KEY] is True or False"""
        self.player.process_move_keys(keys)

    def _move_bar_keys(self, dir) -> None:
        pass

    #########################################
    # Event emitter

    def _emit(self, name: str, value) -> None:
        if not isinstance(name, str):
            e = "Event was not a string"
            traceback.print_tb(e)
            event = Error(e)
            name = event.name
            value = event.value
        for hook in self._hooks.values():
            hook(name, value)

    #########################################
    # Callback methods

    def hook(self, callback):
        """
        Emits events using the value

        `callback(event_name, event_value)`
        """
        self._hook[callback] = callback

    def unhook(self, callback):
        del self._hook[callback]


class DebugRender:
    """Sync instance with Engine"""

    def __init__(self, space, quitcb=lambda _=0: 0, keycb=lambda _=0: 0):
        self.space = space

        # We are going to use a square arena anyway
        self.screen = pygame.display.set_mode((600, 600))

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        # Register callbacks
        self.quitcb = quitcb
        self.keycb = keycb

        self.render_task = self.start_render()

    def start_render(self):
        return asyncio.get_event_loop().create_task(self.update_loop())

    async def update_loop(self):
        try:
            while True:
                t = time.time()
                if not self.update():
                    self.quitcb()
                    return
                # Compensate for the calculation time in tick
                await asyncio.sleep(1 / 60 - (time.time() - t))
        except asyncio.CancelledError:
            print("game closed")
            return

    def update(self):
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                return False
            self.keycb(event.key)
        self.screen.fill("WHITE")
        self.space.debug_draw(self.draw_options)
        pygame.display.update()
        return True

    def destroy(self):
        """Stops all loops and closes pygame"""
        if self.render_task:
            self.render_task.cancel()
        print("destroyed")
