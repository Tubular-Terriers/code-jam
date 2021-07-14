import asyncio
import time

import pygame
import pymunk
import pymunk.pygame_util

from .entities.player import Player
from .events import MoveBar, MovePlayer


class Engine:
    def __init__(self, debug=False):
        """Does not run until `#run` is called"""
        self.created_timestamp = time.time()
        self.running = True
        self.debug_render = None
        self.tickcount = 0

        self._hooks = {}

        self.width = 600
        self.height = 600

        self.tickrate = 20

        self.space = pymunk.Space()
        self.space.gravity = 0, 10

        b = pymunk.Body(1, 1)
        self.space.add(b)
        c = pymunk.Circle(b, 10)
        b.position = (100, 100)
        self.space.add(c)

        print(b, c)

        p = Player()
        p.position = (100, 200)
        self.space.add(*p.tuple)

        self.load_mapdata()

        if debug:

            def process_key(key):
                """Process key events passed from pygame window"""

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
            self.space.add(obj)

    async def run(self):
        self.run_task = asyncio.get_event_loop().create_task(self.run_loop())

    async def run_loop(self):
        try:
            while self.running:
                self.tick()
                await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            print("run loop is terminated")

    def tick(self):
        self.tickcount += 1
        self.space.step(0.05)

    def destroy(self):
        if self.debug_render:
            self.debug_render.destroy()
        if self.run_task:
            self.run_task.cancel()
        print("game exit")

        ##########################
        # REMOVE THIS LINE
        asyncio.get_event_loop().stop()

    ############################
    # Events

    def process_event(self, n, v):
        if MovePlayer.eq(n):
            self.move_player(v)
        elif MoveBar.eq(n):
            self.move_bar(v)

    def move_player(self, dir):
        if dir == MovePlayer.UP:
            pass
        elif dir == MovePlayer.DOWN:
            pass
        elif dir == MovePlayer.LEFT:
            pass
        elif dir == MovePlayer.RIGHT:
            pass

    def move_bar(self, dir):
        if dir == MoveBar.UP:
            pass
        elif dir == MoveBar.DOWN:
            pass
        elif dir == MoveBar.LEFT:
            pass
        elif dir == MoveBar.RIGHT:
            pass

    #########################################
    # Event emitter

    def _emit(self, name, value) -> None:
        for hook in self._hook.values():
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

    def __init__(self, space, quitcb=lambda _: None, keycb=lambda _: None):
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
                if not self.update():
                    self.quitcb()
                    return
                await asyncio.sleep(1 / 60)
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
