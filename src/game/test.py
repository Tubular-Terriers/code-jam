import asyncio
import time

import engine

game = engine.Game()
# game.start()


i = 0
# while True:
#     i += 1
#     game.render.update()
#     time.sleep(0.1)


async def main():
    while True:
        if not game.render.update():
            return
        await asyncio.sleep(0.1)


asyncio.run(main())
