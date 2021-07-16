import asyncio
import random
import time
import traceback

import pygame
import pymunk
import pymunk.pygame_util

from . import category, collision_type
from .entities.ball import Ball
from .entities.player import Player
from .events import Error, MoveBar, MovePlayer, Sound


class Engine:
    def __init__(self, debug=False):
        """Does not run until `#run` is called"""
        self.created_timestamp = time.time()
        self.running = True
        self.debug_render = None
        self.tickcount = 0

        self._hooks = {}
        self._hooks[self.process_event] = self.process_event

        self.entities = {}

        # def c(n, v):
        #     if n == Sound.ID:
        #         print(v)

        # self._hooks[c] = c

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

        self.space.static_body

        # b = pymunk.Body(1, 1)
        # self.space.add(b)
        # c = pymunk.Circle(b, 10)
        # b.position = (100, 100)
        # self.space.add(c)

        # print(b, c)

        p = Player()
        self.player = p
        p.position = (100, 200)
        p.add_space(self.space)

        self.register_entity(p)

        try:
            for i in range(20):
                ball = Ball()
                ball.position = (10 * i + 10, 300)
                ball.velocity = (0, 100)
                ball.angular_velocity = random.random() * 1000
                ball.add_space(self.space)

                self.register_entity(ball)
        except Exception as e:
            print(e)

        # Test bounding box
        bb = pymunk.BB(50, 300, 150, 150)
        # self.space.add(bb)

        self.load_mapdata()

        # Add custom tick method so debug has an option to use it
        self.control = lambda _=0: 0

        # FIXME remove this as this is only used for checking stuff
        self.temp = None

        if debug:

            # Process callbacks
            def process_key(key):
                """Process key events passed from pygame window"""
                if key == pygame.K_SPACE:
                    print("space pressed")
                    self.temp = self.player.dump_data()
                elif key == pygame.K_l:
                    print("loading data")
                    self.player.load_data(self.temp)

            # Process routines
            def routine():
                try:
                    p = pygame.key.get_pressed()
                    keys = {}
                    keys[MovePlayer.UP] = p[pygame.K_w]
                    keys[MovePlayer.DOWN] = p[pygame.K_s]
                    keys[MovePlayer.LEFT] = p[pygame.K_a]
                    keys[MovePlayer.RIGHT] = p[pygame.K_d]
                    keys[MoveBar.UP] = p[pygame.K_UP]
                    keys[MoveBar.DOWN] = p[pygame.K_DOWN]
                    keys[MoveBar.LEFT] = p[pygame.K_LEFT]
                    keys[MoveBar.RIGHT] = p[pygame.K_RIGHT]
                    self._emit(MovePlayer.ID, keys)
                    self._emit(MoveBar.ID, keys)
                except Exception as e:
                    print(e)
                    self._emit(Error.ID, e.message)

            self.control = routine
            self.debug_render = DebugRender(self.space, self.destroy, process_key)

        def on_hitbox_ball_hit(arbiter, space, data):
            """`arbiter.shapes[0]` is hitbox, `arbiter.shapes[1]` is ball"""
            self.space.remove(arbiter.shapes[1])
            self._emit(Sound.ID, Sound.PLAYER_DAMAGE)
            return False

        # ch = self.space.add_collision_handler(collision_type.BALL, collision_type.WALL)
        ch = self.space.add_collision_handler(
            collision_type.HITBOX, collision_type.BALL
        )
        ch.pre_solve = on_hitbox_ball_hit

        def on_collision_ball_hit(arbiter, space, data):
            # TODO: implement ball curving
            self._emit(Sound.ID, Sound.HIT)

        ch_collision_box = self.space.add_collision_handler(
            collision_type.BALL_COLLISION_BOX, collision_type.BALL
        )
        ch_collision_box.post_solve = on_collision_ball_hit

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

            obj.collision_type = collision_type.WALL
            obj.filter = pymunk.ShapeFilter(
                categories=category.WALL, mask=category.MASK.WALL
            )

            self.space.add(obj)

    def register_entity(self, entity):
        self.entities[entity.uuid] = entity

    def remove_entity(self, entity):
        del self.entities[entity.uuid]

    async def run(self):
        # TODO: this method should be synchronous
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

        # For all players, update their bounding box
        # FIXME For now, only update self player
        self.player._update_bar()

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

    def _move_bar_keys(self, keys) -> None:
        self.player.process_bar_keys(keys)

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
            try:
                self.keycb(event.key)
            except AttributeError:
                pass
            except Exception as e:
                print(e)
        self.screen.fill("WHITE")
        self.space.debug_draw(self.draw_options)
        pygame.display.update()
        return True

    def destroy(self):
        """Stops all loops and closes pygame"""
        if self.render_task:
            self.render_task.cancel()
        print("destroyed")
