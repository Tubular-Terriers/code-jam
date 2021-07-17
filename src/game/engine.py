import asyncio
import math
import random
import time
import traceback

import pygame
import pymunk
import pymunk.pygame_util

from . import category, collision_type
from .entities.ball import Ball
from .entities.border import Border
from .entities.entity_type import EntityType
from .entities.player import Player
from .entities.spawner import Spawner
from .events import Error, MoveBar, MovePlayer, Sound


class Engine:
    def __init__(self, debug=False, is_server=True, is_client=True):
        """Does not run until `#run` is called"""
        self.created_timestamp = time.time()
        self.running = True
        self.debug_render = None

        self.is_server = is_server
        self.is_client = True

        self.tickcount = 0

        self._hooks = {}
        self._hooks[self.process_event] = self.process_event

        self.entities = {}
        self.walls = []

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
        self.coroutine = None
        self.ball_body = None

        self.space.static_body.filter = pymunk.ShapeFilter(
            categories=category.WALL, mask=category.MASK.WALL
        )

        self.space.static_body

        self.player = None

        # b = pymunk.Body(1, 1)
        # self.space.add(b)
        # c = pymunk.Circle(b, 10)
        # b.position = (100, 100)
        # self.space.add(c)

        # print(b, c)

        # p = Player()
        # self.player = p
        # p.position = (100, 200)
        # p.add_space(self.space)

        # self.register_entity(p)

        s = Spawner(100)
        s.position = (self.width // 2, self.height // 2)
        s.add_space(self.space)

        self.register_entity(s)

        # try:
        #     self.ball = Ball()
        #     self.ball.position = (10 * 2 + 10, 300)
        #     self.ball.velocity = (0, 100)
        #     self.ball.angular_velocity = random.random() * 1000
        #     self.ball.add_space(self.space)
        #     self.register_entity(self.ball)
        # except Exception as e:
        #     print(e)

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
                if self.player is None:
                    print("there is no player")
                    return
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
            self.remove_entity(arbiter.shapes[1].body)
            self._emit(Sound.ID, Sound.PLAYER_DAMAGE)
            if arbiter.shapes[0].body:
                pass  # HERE HERE
            return False

        ch = self.space.add_collision_handler(collision_type.BALL, collision_type.WALL)
        ch = self.space.add_collision_handler(
            collision_type.HITBOX, collision_type.BALL
        )
        ch.pre_solve = on_hitbox_ball_hit

        def on_collision_ball_hit(arbiter, space, data):
            # TODO: implement ball curving
            self._emit(Sound.ID, Sound.PADDLE_BOUNCE)

            ball = arbiter.shapes[0].body
            player = arbiter.shapes[1].body

            ball.ownerUUID = player.uuid

            def _map(p, x1, x2, dx1, dx2) -> float:  # A simple range mapper
                return ((dx2 - dx1) * ((p - x1) / (x2 - x1))) + dx1

            poly = arbiter.shapes[0]
            collided = arbiter.shapes[1]

            # print("colided: ", collided)
            space_vertices = []
            for v in poly.get_vertices():
                x, y = v.rotated(poly.body.angle) + poly.body.position
                space_vertices.append((x, y))

            cx, cy = arbiter.contact_point_set.points[0].point_a  # Contact points
            # print("Contact Points: (x, y): ", cx, cy)
            # Actual shape corners
            x1, y1 = space_vertices[0]
            x2, y2 = space_vertices[2]
            # print("World Corners (x1, x2): ", x1, x2)
            # print("World Corners (y1, y2): ", y1, y2)

            # Local shpe corners
            lx1, ly1 = x1 - x1, y1 - y1
            lx2, ly2 = x2 - x1, y2 - y1
            lcx, lcy = cx - x1, cy - y1
            # print("Local Corners (x1, x2): ", lx1, lx2)
            # print("Local Corners (y1, y2): ", ly1, ly2)
            # print("Local Contact (x, y): ", lcx, lcy)

            w = abs(lx2 - lx1)  # Width
            h = abs(ly2 - ly1)  # Height
            # print("Width & Height: ", w, h)

            # Biased coordinates
            tx1, tx2 = lx1 - w // 2, lx2 - w // 2
            ty1, ty2 = ly1 - h // 2, ly2 - h // 2
            tcx, tcy = lcx - w // 2, lcy - h // 2

            # print("Biased Range (x1, x2): ", tx1, tx2)
            # print("Biased Range (y1, y2): ", ty1, ty2)
            # print("Biased Contact (x, y): ", tcx, tcy)

            # Angular range
            a1, a2 = -90, 90
            # print("Angular range: ", a1, a2)

            # Interpolated coordinates
            mx, my = _map(tcx, tx1, tx2, a1, a2), _map(tcy, ty1, ty2, a1, a2)
            # print("Mapped: ", mx, my)

            # Setting vector directions manually
            dirx = 1 if mx > 0 else -1
            if x2 - cx == 0:  # Right collision
                mx *= dirx  # Make mx > 0
            elif x2 - cx < 0:  # Left collision
                mx *= -dirx  # Make mx < 0

            diry = 1 if my > 0 else -1
            if y2 - cy == 0:  # Lower collision
                my *= diry  # Make my > 0
            elif y2 - cy < 0:  # Upper collision
                my *= -diry  # Make my < 0
            # print("Directed: ", mx, my)

            magnitude = 70  # In order to get real velocity data
            nx, ny = (
                math.sin(math.radians(mx)) * magnitude,
                math.sin(math.radians(my)) * magnitude,
            )

            # print("Velocity: ", nx, ny)

            collided.body.velocity = nx, ny

        ch_collision_box = self.space.add_collision_handler(
            collision_type.BALL_COLLISION_BOX, collision_type.BALL
        )
        ch_collision_box.post_solve = on_collision_ball_hit

        def on_collision_ball_bounce(arbiter, space, data):
            ball = arbiter.shapes[0].body
            if ball.is_last_bounce():
                self.space.remove(*ball.tuple)
                self.remove_entity(ball)
                # self.space.add_post_step_callback(
                #     self.space._remove_body, self.entities[ball.uuid]
                # )
                # remove the ball
            ball.bounce_count += 1

        ch_collision_wall = self.space.add_collision_handler(
            collision_type.WALL, collision_type.BALL
        )

        ch_collision_wall.post_solve = on_collision_ball_bounce

        def on_collision_ball_strike(arbiter, space, data):  # FIXME change the name
            print("huura")
            return True

        ch_collision_border = self.space.add_collision_handler(
            collision_type.BORDER, collision_type.BALL
        )

        ch_collision_border.post_solve = on_collision_ball_strike

    def update_entity_speed(self, uuid, *amount):
        # HERE HERE
        # FIX THIS
        # self.entities[uuid].velocity = amount
        pass

    def is_player_bordered(self):
        pass

    def add_player(self, uuid=None):
        p = Player(uuid)
        # In the server, this is changed multiple times
        # But it wont matter that much
        self.player = p
        p.position = (100, 200)
        p.add_space(self.space)

        self.register_entity(p)

        return p.uuid

    def load_mapdata(self):
        """
        We are NOT going to pass this through websockets. TLDR; downloading maps is impossible

        This is a method for dividing up modules so code does not get clogged up
        """
        from .default_map import data

        for obj in data:
            # Load the objects into space
            # These are all static objects
            # if isinstance(obj, Border):
            #     self.register_entity(obj)
            #     self.space.add(obj)
            #     print(self.space.bodies)
            #     continue

            obj.body = self.space.static_body

            # Make these bouncy
            obj.elasticity = 1
            obj.friction = 0

            obj.collision_type = collision_type.WALL
            obj.filter = pymunk.ShapeFilter(
                categories=category.WALL, mask=category.MASK.WALL
            )

            self.space.add(obj)
            self.walls.append(obj)

    def register_entity(self, entity):
        self.entities[entity.uuid] = entity

    def remove_entity(self, entity):
        self.entities.pop(entity.uuid)

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
        except Exception as e:
            traceback.print_exc()

    def tick(self):
        # Update global tick count
        self.tickcount += 1

        # For all players, update their bounding box
        # FIXME For now, only update self player
        self.player._update_bar()

        # Do server side updates
        if self.is_server:
            for entity in list(self.entities.values()):
                if entity.type == EntityType.SPAWNER:
                    spawner = entity
                    spawner.cool()
                    if spawner.is_cooled():
                        spawner.spawn_ball(
                            self.space, self.width, self.height, self.register_entity
                        )

        if self.is_client:
            # Do controller
            self.ttc_tick += 1
            if self.ttc_tick == self.ttc:
                self.control()
                self.ttc_tick = 0
            self.space.step(1 / self.tps)

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
        self._hooks[callback] = callback

    def unhook(self, callback):
        self._hooks.pop(callback)


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
