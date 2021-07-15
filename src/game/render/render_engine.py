import pymunk.pygame_util

class RenderEngine:
    """
    Creates instance of renderer

    Parameters:
        space (pymunk.Space): the space to render
    """

    def __init__(self, space, width, height, quiet=False):
        # TODO allow this 600 to be a variable
        self.w = width
        self.h = height
        self.space = space
        self.coroutine = None
        self.entities = {}
        # self.loop = asyncio.get_event_loop()
        if not quiet:
            self.init_pygame()
    """
    async def update_loop(self):
        while True:
            self.update()
            # TODO  find a way to sync this with game tick rate
            await asyncio.sleep(1 / 10)

    """
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))

        # TODO Temporary debug code
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        # self.coroutine = self.loop.create_task(self.update_loop())
        # self.loop.run_until_complete(self.coroutine)

        # self.run

    # TODO implement this later
    def run(self):
        self.running = True
        while self.running:
            # Check for quit
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    self.running = False

            # TODO someone make this rgb
            self.screen.fill(pygame.Color("black"))

    """
    def update(self):
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                return False
        self.screen.fill("GRAY")
        self.space.debug_draw(self.draw_options)
        pygame.display.update()
        self.space.step(0.01)
        return True

    """
space = pymunk.Space()
render = RenderEngine(space,600,600)
render.run()
