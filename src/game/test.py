from render.render_engine import RenderEngine
from map.map_manager import MapManager
from entity_manager import EntityManager
import pygame
import pymunk
import pymunk.pygame_util

GRAY = (220, 220, 220)
space = pymunk.Space()
space.gravity = 0, 0
boundary1 = space.static_body
boundary2 = space.static_body
boundary3 = space.static_body
boundary4 = space.static_body


class App:
    size = 1000, 700

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

            self.screen.fill(GRAY)
            space.debug_draw(self.draw_options)
            pygame.display.update()
            space.step(0.01)

        pygame.quit()


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


if __name__ == "__main__":
    p0, p1 = (0, 0), (1000, 0)
    segment1 = pymunk.Segment(boundary1, p0, p1, 4)
    p0, p1 = (1000, 0), (1000, 700)
    segment2 = pymunk.Segment(boundary2, p0, p1, 4)
    p0, p1 = (1000, 700), (0, 700)
    segment3 = pymunk.Segment(boundary3, p0, p1, 4)
    p0, p1 = (0, 700), (0, 0)
    segment4 = pymunk.Segment(boundary4, p0, p1, 4)

    segment1.elasticity = 1
    segment2.elasticity = 1
    segment3.elasticity = 1
    segment4.elasticity = 1

    player_b = pymunk.Body(mass=1, moment=10)
    player_b.position = (100, 200)

    player = pymunk.Circle(player_b, radius=15)
    player.elasticity = 0.95

    space.add(player, player_b, segment1, segment2, segment3, segment4)

    App().run()
