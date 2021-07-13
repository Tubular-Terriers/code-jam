import pygame
import pymunk
import pymunk.pygame_util
from entity_manager import EntityManager
from map.map_manager import MapManager
from render.render_engine import RenderEngine

GRAY = (220, 220, 220)
space = pymunk.Space()
space.gravity = 0, 0
boundary1 = space.static_body
boundary2 = space.static_body
boundary3 = space.static_body
boundary4 = space.static_body


# game = engine.Game()
# game.start()


class App:
    size = 1000, 700

    # i = 0
    # while True:
    #     i += 1
    #     game.render.update()
    #     time.sleep(0.1)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


# async def main():
#     while True:
#         if not game.render.update():
#             return
#         await asyncio.sleep(0.1)


def entity_test():
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
    print(renderer.entities)

    pygame.quit()


entity_test()


GRAY = (220, 220, 220)
space = pymunk.Space()
space.gravity = 0, -90
b0 = space.static_body


class Sim:
    size = 700, 240

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.image.save(self.screen, 'intro.png')

            self.screen.fill(GRAY)
            space.debug_draw(self.draw_options)
            pygame.display.update()
            space.step(0.01)

        pygame.quit()


if __name__ == '__main__':
    p0, p1 = (0, 0), (700, 0)
    segment = pymunk.Segment(b0, p0, p1, 4)
    segment.elasticity = 1.5

    body = pymunk.Body(mass=1, moment=10)
    body.position = (100, 200)

    circle = pymunk.Circle(body, radius=30)
    circle.elasticity = 0.95
    space.add(body, circle, segment)

    Sim().run()
